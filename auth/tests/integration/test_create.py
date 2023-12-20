import pytest
import psycopg2
import os, dotenv
from datetime import date

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session

from src.auth.criptography import Cryptography
from src.domain.models import Credentials, Profile
from src.adapters.context import Context

dotenv.load_dotenv()

@pytest.fixture
def cryptography_fixture():
    return Cryptography()

@pytest.fixture
def session_factory_fixture():
    database_url = URL.create(
        drivername = "postgresql",
        host = os.getenv("TEST_DATABASE_HOST"),
        port = os.getenv("TEST_DATABASE_PORT"),
        username = os.getenv("TEST_DATABASE_USERNAME"),
        password = os.getenv("TEST_DATABASE_PASSWORD"),
        database = os.getenv("TEST_DATABASE_NAME")
    )

    engine = create_engine(database_url)
    session_factory = sessionmaker(bind=engine)
    yield session_factory
    engine.dispose()


@pytest.fixture
def context_fixture(session_factory_fixture, cryptography_fixture):
    context = Context(session_factory_fixture)
    context.cryptography = cryptography_fixture
    return context

@pytest.fixture
def database_connection_fixture():
    connection = psycopg2.connect(
        host = os.getenv("TEST_DATABASE_HOST"),
        port = os.getenv("TEST_DATABASE_PORT"),
        user = os.getenv("TEST_DATABASE_USERNAME"),
        password = os.getenv("TEST_DATABASE_PASSWORD"),
        database = os.getenv("TEST_DATABASE_NAME")
    )
    return connection

def test_create_user(context_fixture, database_connection_fixture):
    with context_fixture as context:
        context.users.add_user(
            Credentials(
                username = "ericcar",
                email = "eric.m.cardozo@gmail.com",
                password = context.cryptography.hash("password")
            ),

            Profile(
                first_name = "Eric",
                last_name = "Cardozo",
                birthdate = date(1997, 9, 30)
            )
        )

        context.commit()

        try: 
            connection = database_connection_fixture
            cursor = connection.cursor()

            cursor.execute('''
                SELECT * FROM credentials WHERE username = 'ericcar';
            ''')
            credentials = cursor.fetchall()

            cursor.execute('''
                SELECT * FROM profiles WHERE first_name = 'Eric';
            ''')

            profile = cursor.fetchall()

            assert credentials[0][1] == "ericcar"
            assert credentials[0][2] == "eric.m.cardozo@gmail.com"
            assert context.cryptography.verify("password", credentials[0][3])

            assert profile[0][1] == "Eric"
            assert profile[0][2] == "Cardozo"
            assert profile[0][3] == date(1997, 9, 30)
            
        except Exception as error:
            raise AssertionError(f"Test failed: {error}")
        
        finally:
            cursor.execute('''
                DELETE FROM profiles WHERE first_name = 'Eric';
            ''')

            cursor.execute('''
                DELETE FROM credentials WHERE username = 'ericcar';
            ''')

            connection.commit()
            connection.close()
            cursor.close()

    

        