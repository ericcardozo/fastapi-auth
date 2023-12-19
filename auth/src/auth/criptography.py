from passlib.context import CryptContext
from src.domain.services import Cryptography as Service

class Cryptography(Service):
    DEFAULT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, provider : CryptContext = DEFAULT_CONTEXT):
        self.provider = provider

    def hash(self, password : str) -> str:
        return self.provider.hash(password)
    
    def verify(self, password : str, hashed : str) -> bool:
        return self.provider.verify(password, hashed)