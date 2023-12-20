import pytest
from datetime import date
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from src.auth.criptography import Cryptography
from src.adapters.schemas import Credentials, Profile
from src.adapters.context import Context

@pytest.fixture
def cryptography_fixture():
    return Cryptography()

@pytest.fixture
def session_fixture(cryptography_fixture):
    session = UnifiedAlchemyMagicMock()
    session.add_all([
        Credentials(
            username="ericcar",
            email="eric.m.cardozo@gmail.com",
            password=cryptography_fixture.hash("1234")
        ),

        Profile(
            first_name="Eric",
            last_name="Cardozo",
            birthdate=date(1997, 9, 30)
        )
    ])
    return session

@pytest.fixture
def context_fixture(session_fixture, cryptography_fixture):
    context = Context(session_fixture)
    context.cryptography = cryptography_fixture
    return context

from src.domain.models import Credentials, Profile

def test_add_user(context_fixture):
    with context_fixture as context:
        credentials = Credentials(
            username="juansito",
            email="juansito@gmail.com",
            password=context.cryptography.hash("4321")
        )

        profile = Profile(
            first_name="Juan",
            last_name="Sito",
            birthdate=date(1900, 9, 30)
        )

        context.users.add_user(credentials, profile)
        context.commit()