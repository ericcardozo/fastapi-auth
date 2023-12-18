import pytest
from auth.domain.services import Cryptography
from passlib.context import CryptContext

class PasslibCryptography(Cryptography):
    DEFAULT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, provider : CryptContext = DEFAULT_CONTEXT):
        self.provider = provider

    def hash(self, password : str) -> str:
        return self.provider.hash(password)
    
    def verify(self, password : str, hashed : str) -> bool:
        return self.provider.verify(password, hashed)


@pytest.fixture
def cryptography()->Cryptography:
    return PasslibCryptography()

def test_passlib_cryptography(cryptography : Cryptography):
    assert cryptography.hash("password") != "password"
    assert cryptography.verify("password", cryptography.hash("password"))
    assert not cryptography.verify("password", cryptography.hash("wrong_password"))