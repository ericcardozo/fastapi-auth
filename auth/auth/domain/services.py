from passlib.context import CryptContext

class Service:
    pass

DEFAULT_CRYPTOGRAPHY_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Cryptography(Service):
    def __init__(self, context : CryptContext = DEFAULT_CRYPTOGRAPHY_CONTEXT):
        self.context = context

    def hash(self, password: str) -> str:
        return self.context.hash(password)
    
    def verify(self, password: str, hashed: str) -> bool:
        return self.context.verify(password, hashed)
