from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import Question, User
from app.schemas.documents import QuestionResponse

router = APIRouter(tags=["Questions"])


@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: UUID, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> Question:
    question = db.query(Question).join(Question.document).filter(Question.id == question_id, Question.document.has(user_id=current_user.id)).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
