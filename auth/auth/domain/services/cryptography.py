from passlib.context import CryptContext

class Cryptography:
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.context.hash(password)
    
    @classmethod
    def verify(cls, password: str, hash: str) -> bool:
        return cls.context.verify(password, hash)
