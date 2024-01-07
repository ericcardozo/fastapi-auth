from auth.ports.repository import Accounts as Repository
from auth.domain.aggregates import Account
from auth.domain.models import Credentials
from auth.domain.services import Cryptography

class Schema:
    def __init__(self, id : int, username : str, password : str):
        self.id = id
        self.username = username
        self.password = password

class Accounts(Repository):
    def __init__(self):
        self.accounts = set([
            Schema(1, "admin", Cryptography.hash("admin")),
            Schema(2, "user", Cryptography.hash("user"))
        ])

        self.index = 3 

    def create(self, credentials : Credentials) -> Account:
        schema = Schema(self.index, credentials.username, credentials.password.get_secret_value())
        self.accounts.add(schema)
        self.index += 1
        return Account(schema.id, schema.username)
    
    def read(self, **kwargs)-> Account:
        if kwargs.get("id"):
            for account in self.accounts:
                if account.id == kwargs.get("id"):
                    return Account(account.id, account.username)
        elif kwargs.get("username"):
            for account in self.accounts:
                if account.username == kwargs.get("username"):
                    return Account(account.id, account.username)
        return None

    def update(self, id : int, **kwargs) -> Account:
        for account in self.accounts:
            if account.id == id:
                if kwargs.get("username"):
                    account.username = kwargs.get("username")
                if kwargs.get("password"):
                    account.password = kwargs.get("password")
                return Account(account.id, account.username)

    def delete(self, id : int, **kwargs):
        for account in self.accounts:
            if account.id == id:
                schema = account
                
        self.accounts.remove(schema)
                
    def verify(self, credentials: Credentials) -> bool:
        for account in self.accounts:
            if account.username == credentials.username:
                return Cryptography.verify(credentials.password.get_secret_value(), account.password)
        return False
    