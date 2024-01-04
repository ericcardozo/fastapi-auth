from auth.adapters.context import Users
from auth.domain.models import Credentials

import pytest
import psycopg2
import os, dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

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
def context_fixture(session_factory_fixture):
    context = Users(session_factory_fixture)
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

def test_create_account(context_fixture, database_connection_fixture):
    context = context_fixture

    credentials = Credentials(username = "ericcar", password = "123456")

    with context:
        context.accounts.create(credentials)
        context.commit()

    try:
        connection = database_connection_fixture
        cursor = connection.cursor()

        cursor.execute('''
            SELECT * FROM accounts WHERE username = 'ericcar';
        ''')
        
        account = cursor.fetchall()

        assert account[0][1] == "ericcar"
        assert context.accounts.verify(id=account[0][0], password="123456")
            
    except Exception as error:
        raise AssertionError(f"Test failed: {error}")
    
    finally:
        cursor.execute('''
            DELETE FROM accounts WHERE username = 'ericcar';
        ''')

        connection.commit()
        cursor.close()
        connection.close()



def test_read_account(context_fixture, database_connection_fixture):
    context = context_fixture
    try:
        connection = database_connection_fixture
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO accounts (username, password)
            VALUES ('ericcar', '123456');
        ''')

        connection.commit()

        cursor.execute('''
            SELECT id FROM accounts WHERE username = 'ericcar';
        ''')

        with context:
            user = context.accounts.read(username='ericcar')

        assert user.username == "ericcar"

    except Exception as error:
        raise AssertionError(f"Test failed: {error}")
    
    finally:

        cursor.execute('''
            DELETE FROM accounts WHERE username = 'ericcar';
        ''')

        connection.commit()
        cursor.close()
        connection.close()

def test_update_account(context_fixture, database_connection_fixture):
    context = context_fixture

    try:
        connection = database_connection_fixture
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO accounts (username, password)
            VALUES ('ericcar', '123456');
        ''')

        connection.commit()

        cursor.execute('''
            SELECT id FROM accounts WHERE username = 'ericcar';
        ''')

        account = cursor.fetchall()

        with context:
            context.accounts.update(id=account[0][0], username="ericcar2")
            context.commit()

        cursor.execute('''
            SELECT username FROM accounts WHERE id = %s;
        ''', (account[0][0],))

        username = cursor.fetchall()

        assert username[0][0] == "ericcar2"
    
    except Exception as error:
    
        cursor.execute('''
            DELETE FROM accounts WHERE username = 'ericcar';
        ''')

        raise AssertionError(f"Test failed: {error}")

    finally:
        cursor.execute('''
            DELETE FROM accounts WHERE username = 'ericcar2';
        ''')

        connection.commit()
        cursor.close()
        connection.close()




def test_delete_account(context_fixture, database_connection_fixture):
    context = context_fixture

    try:
        connection = database_connection_fixture
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO accounts (username, password)
            VALUES ('ericcar','123456');
        ''')

        connection.commit()

        with context:
            context.accounts.delete(username="ericcar")
            context.commit()        

        cursor.execute('''
            SELECT * FROM accounts WHERE username = 'ericcar';
        ''')
        accounts = cursor.fetchall()
        assert accounts == []
            
    except Exception as error:
        cursor.execute('''
            DELETE FROM accounts WHERE username='ericcar';            
        ''')
        raise AssertionError(f"Test failed: {error}")
    
    finally:
        cursor.close()
        connection.close()
