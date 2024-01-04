from auth.domain.context import Users as Context
from tests.unit.mock.repository import Accounts

class Users(Context):
    def __init__(self):
        self.commited = False

    def __enter__(self):
        self.accounts = Accounts()
        return self

    def commit(self):
        self.commited = True
        pass
    
    def rollback(self):
        pass