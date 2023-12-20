import os, dotenv
import pytest
from infrastructure.setup import Database

dotenv.load_dotenv()

@pytest.fixture
def database_fixture():
    database = Database(
        host = os.getenv("TEST_DATABASE_HOST"),
        port = os.getenv("TEST_DATABASE_PORT"),
        username = os.getenv("TEST_DATABASE_USERNAME"),
        password = os.getenv("TEST_DATABASE_PASSWORD"),
        database = os.getenv("TEST_DATABASE_NAME")
    )
    
    database.migrate()
    yield database

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
    users = Users(session, cryptography)

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
    session.commit()
    session.close()
    
    connection = database_fixture.connection
    cursor = connection.cursor()
    try:
        cursor.execute('''
            SELECT * FROM credentials WHERE username = 'ericcar';
        ''')

        credentials = cursor.fetchall()
        assert credentials[0][0] == 1
        assert credentials[0][1] == 'ericcar'
        assert credentials[0][2] == 'eric.m.cardozo@gmail.com'

        connection.commit()

        cursor.execute('''
            SELECT * FROM profiles WHERE first_name = 'Eric';
        ''')

        profile = cursor.fetchall()

        assert profile[0][1] == 'Eric'
        assert profile[0][2] == 'Cardozo'

    except Exception as error:
        raise AssertionError(f"Test failed: {error}")
    
    finally:
        connection.commit()
        cursor.close()
        database_fixture.drop()
        connection.close()
        





    





