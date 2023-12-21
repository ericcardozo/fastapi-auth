import pytest
from src.auth.services.criptography import Cryptography

@pytest.fixture
def cryptography_fixture():
    return Cryptography()

def test_cryptography(cryptography_fixture : Cryptography):
    password = "1234"
    hashed_password = cryptography_fixture.hash(password)
    assert hashed_password != password

    assert cryptography_fixture.verify(password, hashed_password) == True
    assert cryptography_fixture.verify("12345", hashed_password) == False