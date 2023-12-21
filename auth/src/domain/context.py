from src.domain.repository import Users as Repository
from src.domain.services import Cryptography, Tokenization, Authentication
from abc import ABC, abstractmethod

class Context(ABC):
    users : Repository
    cryptography : Cryptography
    tokenization : Tokenization
    authentication : Authentication

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError