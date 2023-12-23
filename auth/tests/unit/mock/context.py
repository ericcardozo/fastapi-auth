from auth.domain.context import Context
from tests.unit.mock.repository import FakeAccounts

class FakeContext(Context):
    def __init__(self):
        self.commited = False

    def __enter__(self):
        self.accounts = FakeAccounts()
        return self

    def commit(self):
        self.commited = True
        pass
    
    def rollback(self):
        pass
    