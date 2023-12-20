from src.domain.services import Tokenization as Service

from jose import jwt, JWTError, ExpiredSignatureError
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta
import os, dotenv
from typing import Union, Any, List

dotenv.load_dotenv()

class Tokenization(Service):
    algorithm = 'HS256'
    expiration_delta = timedelta(minutes = 15)

    def __init__(self , algorithm : str = None, expiration_delta : timedelta = None):
        if algorithm:
            self.algorithm = algorithm
        if expiration_delta:
            self.expiration_delta = expiration_delta

    def encode(self, subject: Union[str, Any], expires_delta : timedelta = None) -> str:
        if expires_delta is None:
            expires_delta = self.expiration_delta  
    
        expiration = datetime.utcnow() + expires_delta
        to_encode = { "subject": str(subject), "exp" : expiration }
        token = jwt.encode(to_encode ,os.getenv('JWT_SECRET_KEY'), algorithm = self.algorithm)
        return token

    def decode(self, token : str):
        try:
            decoded_token = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms = [self.algorithm])
            return decoded_token
        except ExpiredSignatureError as expired_error:
            raise ValueError("Token has expired") from expired_error
        except JWTError as jwt_error:
            raise ValueError("Invalid token") from jwt_error