import pytest
from datetime import date
from src.domain.models import User, Profile, Credentials

@pytest.fixture
def user():
    profile = Profile(id=1, first_name="John", last_name="Doe", birthdate=date(2000, 1, 1))
    return User(username="johndoe", profile=profile)

def test_user(user : User):
    assert user.username == "johndoe"
    assert user.profile.id == 1
    assert user.profile.first_name == "John"
    assert user.profile.last_name == "Doe"
    assert user.profile.birthdate == date(2000, 1, 1)

@pytest.fixture
def credentials():
    return Credentials(username="johndoe", email="johndoe@example.com", password="password")

def test_credentials(credentials : Credentials):
    assert credentials.username == "johndoe"
    assert credentials.email == "johndoe@example.com"
