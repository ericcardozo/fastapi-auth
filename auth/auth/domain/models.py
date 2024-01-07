from pydantic import BaseModel, SecretStr

class Credentials(BaseModel):
    username: str
    password: SecretStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
