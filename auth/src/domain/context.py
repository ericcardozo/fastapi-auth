from src.domain.repository import Users
from src.domain.services import Cryptography
from abc import ABC, abstractmethod

class Context(ABC):
    users : Users
    cryptography : Cryptography

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