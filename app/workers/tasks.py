from datetime import datetime, timezone
from uuid import UUID
from app.core.database import SessionLocal
from app.models import AnswerKey, Document, DocumentStatus, Question, Warning
from app.services.extractor import extract_document_text
from app.services.parser import parse_questions
from app.workers.celery_app import celery


@celery.task(name="process_document")
def process_document(document_id: str) -> None:
    db = SessionLocal()
    document = db.get(Document, UUID(document_id))
    if not document:
        db.close()
        return
    try:
        document.status = DocumentStatus.processing
        db.commit()
        text, quality, _ = extract_document_text(document.path, document.file_type)
        questions, warnings, answers = parse_questions(text, quality)
        for parsed in questions:
            db.add(Question(document_id=document.id, question_number=parsed.number, question_text=parsed.text, options=parsed.options, answer=parsed.answer, confidence=parsed.confidence, review_required=parsed.review_required, source_pages=parsed.source_pages, question_type=parsed.question_type))
        for number, answer in answers.items():
            db.add(AnswerKey(document_id=document.id, question_number=number, answer=answer, confidence=0.9, source_page=1))
        for item in warnings:
            db.add(Warning(document_id=document.id, **item))
        if quality < 0.6:
            db.add(Warning(document_id=document.id, warning_type="LOW_OCR_QUALITY", message="OCR confidence is low", confidence=quality))
        document.status = DocumentStatus.completed
        document.completed_at = datetime.now(timezone.utc)
        db.commit()
    except Exception as exc:
        db.rollback()
        document.status = DocumentStatus.failed
        document.error_message = str(exc)[:2000]
        db.commit()
        raise
    finally:
        db.close()
