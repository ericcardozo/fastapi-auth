from pydantic_settings import BaseSettings
from typing import Union, Any

class Settings(BaseSettings):
    database_url : Union[str, Any]