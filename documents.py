from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    status: str
    file_type: str
    error_message: str | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class Option(BaseModel):
    label: str
    text: str


class QuestionResponse(BaseModel):
    id: UUID
    document_id: UUID
    question_number: str
    question_text: str
    question_type: str
    options: list[Option] = Field(default_factory=list)
    answer: str | None = None
    confidence: float
    review_required: bool
    source_pages: list[int]
    warnings: list[str] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class AnswerResponse(BaseModel):
    question_number: str
    answer: str
    confidence: float
    source_page: int | None
    model_config = ConfigDict(from_attributes=True)


class WarningResponse(BaseModel):
    warning_type: str
    message: str
    confidence: float
    model_config = ConfigDict(from_attributes=True)


class RelationCreate(BaseModel):
    related_document_id: UUID
    relationship_type: str = Field(min_length=1, max_length=50)


class RelationResponse(RelationCreate):
    id: UUID
    document_id: UUID
    model_config = ConfigDict(from_attributes=True)
