import os, dotenv
import pytest
from infrastructure.setup import Database

@pytest.fixture
def database_fixture():
    dotenv.load_dotenv()
    database = Database(
        host = os.getenv("TEST_DATABASE_HOST"),
        port = os.getenv("TEST_DATABASE_PORT"),
        username = os.getenv("TEST_DATABASE_USERNAME"),
        password = os.getenv("TEST_DATABASE_PASSWORD"),
        database = os.getenv("TEST_DATABASE_NAME")
    )
    database.migrate()
    yield database
    database.drop()
    database.close()

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from datetime import date

from src.domain.models import Credentials, Profile
from src.adapters.repository import Users


from src.domain.services import Cryptography as Service
from passlib.context import CryptContext

class Cryptography(Service):
    DEFAULT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, provider : CryptContext = DEFAULT_CONTEXT):
        self.provider = provider

    def hash(self, password : str) -> str:
        return self.provider.hash(password)
    
    def verify(self, password : str, hashed : str) -> bool:
        return self.provider.verify(password, hashed)


@pytest.fixture
def orm_engine_fixture():
    dotenv.load_dotenv()
    engine = create_engine(url = URL.create(
        drivername=os.getenv("TEST_DATABASE_DRIVERNAME"),
        username=os.getenv("TEST_DATABASE_USERNAME"),
        password=os.getenv("TEST_DATABASE_PASSWORD"),
        host=os.getenv("TEST_DATABASE_HOST"),
        port=os.getenv("TEST_DATABASE_PORT"),
        database=os.getenv("TEST_DATABASE_NAME")
    ))

    yield engine
    engine.dispose()

def test_add_user(database_fixture : Database, orm_engine_fixture):
    session = sessionmaker(orm_engine_fixture)()
    cryptography = Cryptography()
    users = Users(session, Cryptography())

    credentials = Credentials(
        username="ericcar",
        email="eric.m.cardozo@gmail.com", 
        password=cryptography.hash("1234")
    )

    profile = Profile(
        first_name="Eric",
        last_name="Cardozo",
        birthdate=date(1997, 9, 30)
    )
                              
    users.add_user(credentials, profile)
    
    connection = database_fixture.connection
    cursor = connection.cursor()

    cursor.close()
    session.close()



    





