from app.api.documents import ALLOWED_SUFFIXES, ALLOWED_TYPES


def test_upload_allowlist_is_restricted_to_supported_formats():
    assert ALLOWED_TYPES == {"application/pdf", "image/jpeg", "image/png"}
    assert ALLOWED_SUFFIXES == {".pdf", ".jpg", ".jpeg", ".png"}
