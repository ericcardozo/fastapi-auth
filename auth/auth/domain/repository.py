from abc import ABC, abstractmethod
from typing import TypeVar, Generic, overload
from auth.domain.aggregates import Account

T = TypeVar('T')
class Repository(ABC, Generic[T]):

    @abstractmethod
    def create(self,*args,**kwargs) -> T:
        pass
    
    @abstractmethod
    def read(self, **kwargs) -> T:
        pass

    @abstractmethod
    def update(self,*args, **kwargs) -> T:
        pass

    @abstractmethod
    def delete(self, **kwargs) -> None:
        pass
    
class Accounts(Repository[Account]):
    
    @abstractmethod
    def verify(self, id : int, password : str) -> bool:
        pass