from src.domain.repository import Users as Repository
from src.domain.services import Cryptography
from src.adapters.schemas import Credentials, Profile
from sqlalchemy.orm import Session
from datetime import date

class Users(Repository[Credentials, Profile]):
    def __init__(self, session : Session, criptography : Cryptography):
        super().__init__(criptography)
        self._session = session
        
    def _create_credentials(self, username : str, email : str, password : str) -> int:
        credentials = Credentials(username=username, email=email, password=password)
        self._session.add(credentials)
        self._session.flush()
        return credentials.id
    
    def _create_profile(self, id : int, first_name : str, last_name : str, birthdate : date):
        profile = Profile(id=id, first_name=first_name, last_name=last_name, birthdate=birthdate)
        self._session.add(profile)
        self._session.flush()

    