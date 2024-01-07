import os, dotenv
from typing import Union, Any
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta

class Cryptography:
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.context.hash(password)
    
    @classmethod
    def verify(cls, password: str, hash: str) -> bool:
        return cls.context.verify(password, hash)

class Tokenization:
    dotenv.load_dotenv()
    algorithm = 'HS256'
    expiration_delta = timedelta(minutes = 15)

    @classmethod
    def encode(cls, subject: Union[str, Any], expires_delta : timedelta = expiration_delta) -> dict[str, str]:
        expiration = datetime.utcnow() + expires_delta
        to_encode = { "subject": str(subject), "exp" : expiration }
        encoded = jwt.encode(to_encode ,os.getenv('JWT_SECRET_KEY'), algorithm = cls.algorithm)
        token = { "access_token": encoded, "token_type": "bearer"}
        return token

    @classmethod
    def decode(cls, token : dict[str, str]) -> dict:
        try:
            decoded_token = jwt.decode(token["access_token"], os.getenv('JWT_SECRET_KEY'), algorithms = [cls.algorithm])
            return decoded_token
        
        except ExpiredSignatureError as expired_error:
            raise ValueError("Token has expired") from expired_error
        
        except JWTError as jwt_error:
            raise ValueError("Invalid token") from jwt_error