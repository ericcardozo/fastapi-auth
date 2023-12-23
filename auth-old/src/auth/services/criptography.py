from passlib.context import CryptContext
from src.domain.services import Cryptography as Service

class Cryptography(Service):
    def __init__(self, context : CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")):
        self.context = context

    def hash(self, password : str) -> str:
        return self.context.hash(password)
    
    def verify(self, password : str, hashed : str) -> bool:
        return self.context.verify(password, hashed)