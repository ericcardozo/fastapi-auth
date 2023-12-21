from abc import ABC, abstractmethod

class Cryptography(ABC):
    @abstractmethod
    def hash(self, password : str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, password : str, hashed : str) -> bool:
        raise NotImplementedError
    
    
class Tokenization(ABC):
    @abstractmethod
    def encode(self, data : dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token : str) -> dict:
        raise NotImplementedError
    
    
class Authentication(ABC):
    @abstractmethod
    def login(self, username : str, password : str) -> str:
        raise NotImplementedError