"""initial schema"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    document_status = sa.Enum("uploaded", "processing", "completed", "failed", name="documentstatus")
    document_status.create(op.get_bind(), checkfirst=True)
    op.create_table("users", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("email", sa.String(320), nullable=False, unique=True), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("documents", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("filename", sa.String(255), nullable=False), sa.Column("path", sa.String(1024), nullable=False), sa.Column("status", document_status, nullable=False), sa.Column("file_type", sa.String(100), nullable=False), sa.Column("error_message", sa.Text), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("completed_at", sa.DateTime(timezone=True)))
    op.create_table("questions", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("question_number", sa.String(50), nullable=False), sa.Column("question_text", sa.Text, nullable=False), sa.Column("options", postgresql.JSONB), sa.Column("answer", sa.String(255)), sa.Column("confidence", sa.Float, nullable=False), sa.Column("review_required", sa.Boolean, nullable=False), sa.Column("source_pages", postgresql.JSONB, nullable=False), sa.Column("question_type", sa.String(30), nullable=False), sa.UniqueConstraint("document_id", "question_number"))
    op.create_table("answer_keys", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("question_number", sa.String(50), nullable=False), sa.Column("answer", sa.String(255), nullable=False), sa.Column("confidence", sa.Float, nullable=False), sa.Column("source_page", sa.Integer))
    op.create_table("warnings", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("warning_type", sa.String(50), nullable=False), sa.Column("message", sa.Text, nullable=False), sa.Column("confidence", sa.Float, nullable=False))
    op.create_table("document_relationships", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("related_document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("relationship_type", sa.String(50), nullable=False))


def downgrade() -> None:
    for table in ("document_relationships", "warnings", "answer_keys", "questions", "documents", "users"):
        op.drop_table(table)
    sa.Enum(name="documentstatus").drop(op.get_bind(), checkfirst=True)
