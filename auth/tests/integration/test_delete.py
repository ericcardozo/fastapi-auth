import pytest
import psycopg2
import os, dotenv
from datetime import date

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session

from src.auth.services.criptography import Cryptography
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

def test_delete(context_fixture, database_connection_fixture):
    context = context_fixture

    try:
        connection = database_connection_fixture
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO credentials (username, email, password)
            VALUES ('ericcar', 'eric.m.car@gmail.com', '123456');
        ''')

        connection.commit()


        cursor.execute('''
            SELECT id FROM credentials WHERE username = 'ericcar';
        ''')

        id = cursor.fetchall()[0]

        cursor.execute('''
            INSERT INTO profiles (id, first_name, last_name, birthdate)
            VALUES (%s, 'Eric', 'Cardozo', '1997-09-30');
        ''', (id))

        connection.commit()

        #TODO: Use decorator to inject the crud operation

        with context:
            context.users.remove_user_by_username("ericcar")
            context.commit()        

        cursor.execute('''
            SELECT * FROM credentials WHERE username = 'ericcar';
        ''')
        credentials = cursor.fetchall()

        cursor.execute('''
            SELECT * FROM profiles WHERE first_name = 'Eric';
        ''')

        profile = cursor.fetchall()

        assert credentials == []
        assert profile == []
            
    except Exception as error:
        raise AssertionError(f"Test failed: {error}")
    
    finally:
        cursor.close()
        connection.close()