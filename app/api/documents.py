from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_owned_document
from app.core.config import settings
from app.core.database import get_db
from app.models import AnswerKey, Document, DocumentRelationship, DocumentStatus, Question, User, Warning
from app.schemas.documents import AnswerResponse, DocumentResponse, QuestionResponse, RelationCreate, RelationResponse, WarningResponse
from app.workers.tasks import process_document

router = APIRouter(prefix="/documents", tags=["Documents"])
ALLOWED_TYPES = {"application/pdf", "image/jpeg", "image/png"}
ALLOWED_SUFFIXES = {".pdf", ".jpg", ".jpeg", ".png"}


def owned_document(document_id: UUID, current_user: User, db: Session) -> Document:
    document = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.post("", response_model=DocumentResponse, status_code=202)
def upload_document(file: Annotated[UploadFile, File(...)], current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> Document:
    suffix = Path(file.filename or "").suffix.lower()
    if file.content_type not in ALLOWED_TYPES or suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=415, detail="Only PDF, JPG, JPEG, and PNG files are supported")
    data = file.file.read(settings.max_file_size_mb * 1024 * 1024 + 1)
    if len(data) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds the size limit")
    document_id = uuid4()
    path = settings.upload_path / f"{document_id}{suffix}"
    path.write_bytes(data)
    document = Document(id=document_id, user_id=current_user.id, filename=file.filename or path.name, path=str(path), file_type=file.content_type, status=DocumentStatus.uploaded)
    db.add(document)
    db.commit()
    db.refresh(document)
    process_document.delay(str(document.id))
    return document


@router.get("", response_model=list[DocumentResponse])
def list_documents(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> list[Document]:
    return db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document: Annotated[Document, Depends(get_owned_document)]) -> Document:
    return document


@router.get("/{document_id}/status", response_model=DocumentResponse)
def document_status(document: Annotated[Document, Depends(get_owned_document)]) -> Document:
    return document


@router.delete("/{document_id}", status_code=204)
def delete_document(document: Annotated[Document, Depends(get_owned_document)], db: Annotated[Session, Depends(get_db)]) -> None:
    path = Path(document.path)
    db.delete(document)
    db.commit()
    path.unlink(missing_ok=True)


@router.get("/{document_id}/questions", response_model=list[QuestionResponse])
def questions(document: Annotated[Document, Depends(get_owned_document)], db: Annotated[Session, Depends(get_db)]) -> list[Question]:
    return db.query(Question).filter(Question.document_id == document.id).order_by(Question.question_number).all()


@router.get("/{document_id}/answers", response_model=list[AnswerResponse])
def answers(document: Annotated[Document, Depends(get_owned_document)], db: Annotated[Session, Depends(get_db)]) -> list[AnswerKey]:
    return db.query(AnswerKey).filter(AnswerKey.document_id == document.id).all()


@router.get("/{document_id}/warnings", response_model=list[WarningResponse])
def warnings(document: Annotated[Document, Depends(get_owned_document)], db: Annotated[Session, Depends(get_db)]) -> list[Warning]:
    return db.query(Warning).filter(Warning.document_id == document.id).all()


@router.post("/{document_id}/relations", response_model=RelationResponse, status_code=201)
def add_relation(document: Annotated[Document, Depends(get_owned_document)], payload: RelationCreate, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> DocumentRelationship:
    related = owned_document(payload.related_document_id, current_user, db)
    if related.id == document.id:
        raise HTTPException(status_code=400, detail="A document cannot relate to itself")
    relation = DocumentRelationship(document_id=document.id, related_document_id=related.id, relationship_type=payload.relationship_type)
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


@router.get("/{document_id}/relations", response_model=list[RelationResponse])
def relations(document: Annotated[Document, Depends(get_owned_document)], db: Annotated[Session, Depends(get_db)]) -> list[DocumentRelationship]:
    return db.query(DocumentRelationship).filter(DocumentRelationship.document_id == document.id).all()
