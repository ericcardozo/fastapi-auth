from pydantic.dataclasses import dataclass

class Command:
    pass

@dataclass
class LogginUser(Command):
    username: str
