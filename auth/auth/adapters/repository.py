from auth.domain.repository import Accounts
from auth.domain.aggregates import Account
from auth.domain.services import Cryptography
from auth.adapters.schemas import AccountSchema
from sqlalchemy.orm import Session

class AccountsRepository(Accounts):
    def __init__(self, session : Session):
        self.session = session

    def create(self, username : str, password : str) -> Account:
        self.session.add(AccountSchema(
            username = username,
            password = password,
        ))

        account_schema = self.session.query(AccountSchema).filter_by(username=username).first()
        
        return Account(
            id = account_schema.id,
            username = username
        )
    
    def read(self, **kwargs) -> Account:
        account_schema = self.session.query(AccountSchema).filter_by(**kwargs).first()
        return Account(
            id = account_schema.id,
            username = account_schema.username 
        ) if account_schema else None

    def update(self, id : int, **kwargs) -> Account:
        self.session.query(AccountSchema).update(kwargs)
        account_schema = self.session.query(AccountSchema).filter_by(id=id).first()
        return Account(
            id = account_schema.id,
            username = account_schema.username
        ) if account_schema else None
    
    def delete(self, **kwargs) -> None:
        account_schema = self.session.query(AccountSchema).filter_by(**kwargs).first()
        if account_schema:
            self.session.delete(account_schema)
        
    def verify(self, id : int, password : str) -> bool:
        account_schema = self.session.query(AccountSchema).filter_by(id=id).first()
        return Cryptography.verify(password, account_schema.password)

        