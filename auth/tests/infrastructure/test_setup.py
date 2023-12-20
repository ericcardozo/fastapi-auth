import os, dotenv
import pytest
from infrastructure.setup import Database
from datetime import date

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

def test_database(database_fixture : Database):
    connection = database_fixture.connection
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO credentials (username, email, password)
            VALUES ('ericcar', 'eric.m.cardozo@gmail.com', '1234');            
        ''')
        connection.commit()

        cursor.execute('''
            SELECT * FROM credentials WHERE username = 'ericcar';
        ''')

        credentials = cursor.fetchall()
        assert credentials[0][1] == 'ericcar'
        assert credentials[0][2] == 'eric.m.cardozo@gmail.com'

        cursor.execute('''
            INSERT INTO profiles (id, first_name, last_name, birthdate)
            VALUES (1, 'Eric', 'Cardozo', '1997-09-30')
        ''')

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
        database_fixture.connection.close()



    



    
