import pytest
from auth.domain.services import Cryptography, CryptContext

@pytest.fixture
def cryptography():
    return Cryptography(CryptContext(schemes=["bcrypt"], deprecated="auto"))

def test_cryptography(cryptography : Cryptography):
    assert cryptography.hash("password") != "password"
    assert cryptography.verify("password", cryptography.hash("password"))
    assert not cryptography.verify("password", cryptography.hash("wrong_password"))