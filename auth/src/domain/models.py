from pydantic import BaseModel, SecretStr, EmailStr
from datetime import date

class Profile(BaseModel):
    first_name : str
    last_name : str
    birthdate : date

class Credentials(BaseModel):
    username : str
    email : EmailStr
    password : SecretStr

class User:
    def __init__(self, id : int, username : str, profile : Profile):
        self.id = id
        self.username = username
        self.profile = profile