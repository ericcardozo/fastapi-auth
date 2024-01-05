from abc import ABC, abstractmethod

from auth.domain.aggregates import Profile
from auth.domain.models import Info

class Profiles(ABC):

    @abstractmethod
    def create(self, id : int, info : Info) -> Profile:
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass