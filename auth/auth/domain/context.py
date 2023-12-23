from abc import ABC, abstractmethod
from auth.domain.repository import Accounts
from auth.domain.services import Cryptography, Tokenization

class Context(ABC):
    accounts : Accounts
    cryptography = Cryptography()
    tokenization = Tokenization()   

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError