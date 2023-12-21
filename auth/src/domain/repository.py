from datetime import date
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.domain.models import User, Profile, Credentials, SecretStr
from src.domain.services import Cryptography

C, P = TypeVar('C'), TypeVar('P')
class Users(ABC, Generic[C,P]):
    def __init__(self):
        pass

    @abstractmethod
    def _create_credentials(self, **kwargs) -> int:    
        raise NotImplementedError

    @abstractmethod
    def _create_profile(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def _read_credentials(self, **kwargs) -> C:
        raise NotImplementedError
    
    @abstractmethod
    def _read_profile(self, **kwargs) -> P:
        raise NotImplementedError
    
    @abstractmethod
    def _delete_user(self, id : int):
        raise NotImplementedError
    
    def add_user(self, credentials : Credentials, profile : Profile) -> int:
        id = self._create_credentials(
            username = credentials.username,
            email = credentials.email,
            password= credentials.password.get_secret_value() )
        
        
        self._create_profile(
            id = id,
            first_name = profile.first_name,
            last_name = profile.last_name,

            birthdate = profile.birthdate )
        return id
    
    def get_user_by_username(self, username : str) -> User:
        credentials = self._read_credentials(username=username)
        profile = self._read_profile(id=credentials.id)
        profile_model = Profile(
            first_name = profile.first_name,
            last_name = profile.last_name,
            birthdate = profile.birthdate
        )
        user = User(id = credentials.id, username = credentials.username, profile = profile_model)
        return user
    
    def remove_user_by_id(self, id : int):
        self._delete_user(id=id)

    def remove_user_by_username(self, username : str):
        self._delete_user(username=username)
    
        
