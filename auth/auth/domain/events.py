from pydantic.dataclasses import dataclass

class Event:
    pass

@dataclass
class UserLoggedIn(Event):
    pass

@dataclass
class UserSignedUp(Event):
    pass