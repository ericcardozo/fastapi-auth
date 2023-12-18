from datetime import date
from auth.domain.models import User, Profile, Credentials
from auth.domain.services import Cryptography
from auth.domain.repository import Users
from passlib.context import CryptContext

class PasslibCryptography(Cryptography):
    DEFAULT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, provider : CryptContext = DEFAULT_CONTEXT):
        self.provider = provider

    def hash(self, password : str) -> str:
        return self.provider.hash(password)
    
    def verify(self, password : str, hashed : str) -> bool:
        return self.provider.verify(password, hashed)
    
class FakeCredentialsORM:
    def __init__(self, id : int, username : str, email : str, password : str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class FakeProfileORM:
    def __init__(self, id : int, first_name : str, last_name : str, birthdate : date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate

class FakeUser:
    def __init__(self, username : str, profile : Profile):
        self.username = username
        self.profile = profile


class FakeUsers(Users[FakeCredentialsORM, FakeProfileORM]):
    def __init__(self, cryptography : Cryptography):
        super().__init__(cryptography)
        self.credentials = []
        self.profiles = []
        self.id = 1

    def _create_credentials(self, username : str, email : str, password : str) -> int:
        id = self.id
        self.id += 1
        self.credentials.append(FakeCredentialsORM(id, username, email, password))
        return id

    def _create_profile(self, id : int, first_name : str, last_name : str, birthdate : date):
        self.profiles.append(FakeProfileORM(id, first_name, last_name, birthdate))

import pytest

@pytest.fixture
def users():
    return FakeUsers(PasslibCryptography())

@pytest.fixture
def credentials():
    return Credentials(username="johndoe", email="johndoe@example.com", password="password")

def test_fake_users_create(users, credentials):
    assert len(users.credentials) == 0
    assert len(users.profiles) == 0

    user_id = users.add_user(credentials, Profile(id=1, first_name="John", last_name="Doe", birthdate=date(2000, 1, 1)))

    assert len(users.credentials) == 1
    assert len(users.profiles) == 1

    added_credentials = users.credentials[0]
    added_profile = users.profiles[0]

    assert added_credentials.username == "johndoe"
    assert added_credentials.email == "johndoe@example.com"

    assert added_profile.id == 1
    assert added_profile.first_name == "John"
    assert added_profile.last_name == "Doe"
    assert added_profile.birthdate == date(2000, 1, 1)

    assert user_id != 0