from types import SimpleNamespace
from uuid import uuid4
import pytest
from app.api.documents import owned_document


def test_document_access_requires_matching_owner():
    document = SimpleNamespace(id=uuid4(), user_id=uuid4())
    user = SimpleNamespace(id=uuid4())
    db = SimpleNamespace(query=lambda model: None)
    with pytest.raises(Exception):
        owned_document(document.id, user, db)
