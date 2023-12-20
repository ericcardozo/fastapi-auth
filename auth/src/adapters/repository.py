from src.domain.repository import Users as Repository
from src.domain.services import Cryptography
from src.adapters.schemas import Credentials, Profile
from sqlalchemy.orm import Session, sessionmaker
from datetime import date

class Users(Repository[Credentials, Profile]):
    def __init__(self, session : Session):
        self._session = session

    #TODO: Change the parameters to **kwargs in creation.
        
    def _create_credentials(self, username : str, email : str, password : str) -> int:
        credentials = Credentials(username=username, email=email, password=password)
        self._session.add(credentials)
        self._session.flush()
        return credentials.id
    
    def _create_profile(self, id : int, first_name : str, last_name : str, birthdate : date):
        profile = Profile(id=id, first_name=first_name, last_name=last_name, birthdate=birthdate)
        self._session.add(profile)
        self._session.flush()

    def _read_credentials(self, **kwargs) -> Credentials:
        return self._session.query(Credentials).filter_by(**kwargs).first()

    def _read_profile(self, **kwargs) -> Profile:
        return self._session.query(Profile).filter_by(**kwargs).first()
    
    def _delete_user(self, **kwargs):
        user = self._session.query(Credentials).filter_by(**kwargs).first()
        id = user.id
        self._session.query(Profile).filter_by(id=id).delete()
        self._session.query(Credentials).filter_by(id=id).delete()

    