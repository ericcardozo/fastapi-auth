from abc import ABC, abstractmethod

class Service:
    pass

class Cryptography(ABC, Service):
    @abstractmethod
    def hash(self, password : str) -> str:
        pass

    @abstractmethod
    def verify(self, password : str, hashed : str) -> bool:
        pass