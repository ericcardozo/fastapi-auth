from pydantic.dataclasses import dataclass

class Event:
    pass

@dataclass
class UserLoggedIn(Event):
    username: str