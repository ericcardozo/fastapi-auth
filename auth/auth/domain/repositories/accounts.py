from abc import ABC, abstractmethod

from auth.domain.aggregates import Account
from auth.domain.models import Credentials
    
class Accounts(ABC):

    @abstractmethod
    def create(self, credentials : Credentials) -> Account:
        pass
    
    @abstractmethod
    def read(self, **kwargs) -> Account:
        pass

    @abstractmethod
    def update(self, id : int, **kwargs) -> Account:
        pass

    @abstractmethod
    def delete(self, **kwargs) -> None:
        pass

    @abstractmethod
    def verify(self, credentials : Credentials) -> bool:
        pass