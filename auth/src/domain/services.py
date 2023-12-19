from abc import ABC, abstractmethod

class Cryptography(ABC):
    @abstractmethod
    def hash(self, password : str) -> str:
        pass

    @abstractmethod
    def verify(self, password : str, hashed : str) -> bool:
        pass