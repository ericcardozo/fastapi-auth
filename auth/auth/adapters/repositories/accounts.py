from sqlalchemy.orm import Session

from auth.domain.repositories.accounts import Accounts as Repository
from auth.domain.aggregates import Account
from auth.domain.models import Credentials
from auth.domain.services.cryptography import Cryptography
from auth.adapters.schemas import Account as Schema

class Accounts(Repository):
    def __init__(self, session : Session):
        self.session = session

    def create(self, credentials : Credentials) -> Account:
        schema = Schema(
            username = credentials.username,
            password = Cryptography.hash(credentials.password.get_secret_value()),
        )

        self.session.add(schema)
        account_schema = self.session.query(Schema).filter_by(username=credentials.username).first()        
        return Account(id = account_schema.id, username = credentials.username)
    
    def read(self, **kwargs) -> Account:
        schema = self.session.query(Schema).filter_by(**kwargs).first()
        return Account(id = schema.id, username = schema.username) if schema else None

    def update(self, id : int, **kwargs) -> Account:
        self.session.query(Schema).update(kwargs)
        schema = self.session.query(Schema).filter_by(id=id).first()
        return Account(id = schema.id, username = schema.username) if schema else None
    
    def delete(self, **kwargs) -> None:
        schema = self.session.query(Schema).filter_by(**kwargs).first()
        if schema:
            self.session.delete(schema)
        
    def verify(self, id : int, password : str) -> bool:
        account_schema = self.session.query(Schema).filter_by(id=id).first()
        return Cryptography.verify(password, account_schema.password)