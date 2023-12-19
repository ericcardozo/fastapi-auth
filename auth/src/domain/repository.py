from datetime import date
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.domain.models import User, Profile, Credentials, SecretStr
from src.domain.services import Cryptography

C, P = TypeVar('C'), TypeVar('P')
class Users(ABC, Generic[C,P]):
    def __init__(self, cryptography : Cryptography):
        self.cryptography = cryptography

    @abstractmethod
    def _create_credentials(self, username : str, email : str, password : str) -> int:
        pass

    @abstractmethod
    def _create_profile(self, id : int, first_name : str, last_name : str, birthdate : date):
        pass

    def add_user(self, credentials : Credentials, profile : Profile) -> int:
        id = self._create_credentials(credentials.username, credentials.email, credentials.password.get_secret_value())
        self._create_profile(id, profile.first_name, profile.last_name, profile.birthdate)
        return id
