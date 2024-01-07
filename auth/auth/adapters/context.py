from sqlalchemy.orm import sessionmaker, Session

from auth.ports.context import Users as Context
from auth.adapters.repository import Accounts

class Users(Context):
    def __init__(self, session_factory : sessionmaker):
        self.session_factory = session_factory 
        self.session : Session

    def __enter__(self):
        self.session = self.session_factory()
        self.accounts = Accounts(self.session)  
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close() 

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()