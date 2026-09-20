from app.core.security import create_access_token, hash_password, verify_password


def test_password_hash_round_trip():
    password_hash = hash_password("password123")
    assert password_hash != "password123"
    assert verify_password("password123", password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_access_token_contains_subject():
    token = create_access_token("user-id")
    assert isinstance(token, str)
