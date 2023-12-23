from auth.domain.repository import Accounts
from auth.domain.aggregates import Account
from auth.domain.services import Cryptography

class FakeAccounts(Accounts):
    
    def __init__(self):
        self.accounts = set([
            Account(1, "admin"),
            Account(2, "user")])
        
        self.passwords = {
            1 : Cryptography.hash("admin"),
            2 : Cryptography.hash("user")
        }
        
        self.index = 3

    def create(self, username : str, password : str) -> Account:
        account = Account(self.index, username)
        self.index += 1
        self.accounts.add(account)
        return account
    
    def read(self, **kwargs) -> Account:
        key, value = next(iter(kwargs.items()))
        if key == 'username':
            return next((account for account in self.accounts if account.username == value), None)
        elif key == 'id':
            return next((account for account in self.accounts if account.id == value), None)
        else:
            return None
        
    def update(self, id : int, **kwargs) -> Account:
        account = next((account for account in self.accounts if account.id == id), None)
        if account:
            for key, value in kwargs.items():
                if key == 'username':
                    account.username = value
        return account

    def delete(self, **kwargs) -> None:
        key, value = next(iter(kwargs.items()))
        if key == 'username':
            account = next((account for account in self.accounts if account.username == value), None)
            if account:
                self.accounts.remove(account)
        elif key == 'id':
            account = next((account for account in self.accounts if account.id == value), None)
            if account:
                self.accounts.remove(account)
        else:
            return None
        
    def verify(self, id : int, password : str) -> bool:
        return Cryptography.verify(password, self.passwords[id])
        
