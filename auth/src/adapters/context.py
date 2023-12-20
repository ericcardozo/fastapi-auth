from src.domain.context import Context as Provider
from src.domain.services import Cryptography
from src.adapters.repository import Users
from sqlalchemy.orm import sessionmaker, Session

class Context(Provider):
    def __init__(self, session_factory : sessionmaker):
        self.session_factory = session_factory 
        self.session : Session

    def __enter__(self):
        self.session = self.session_factory()
        self.users = Users(self.session)  
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close() 

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
