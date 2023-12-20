import os, dotenv
from typing import List
import psycopg2

dotenv.load_dotenv()
class Database:        
    def __init__(self, host : str, port : str, username : str, password : str, database : str):
        try:
            self.connection = psycopg2.connect(
                host = host,
                port = port,
                user = username,
                password = password,
                database = database
            )
        
        except Exception as error:
            self.connection = None
            print("Error while connecting to database", error)

    def migrate(self):
        path = os.path.abspath("infrastructure/migrations") 
        print(path)
        assert self.connection is not None, "Database connection is not established"
        cursor = self.connection.cursor()
        migrations = os.listdir(path)
        for migration in sorted(migrations):
            with open(os.path.join(path, migration), "r") as file:
                sql = file.read()
                cursor.execute(sql)
                self.connection.commit()
                print(f"Migration {migration} executed successfully")
        cursor.close()

    def drop(self, tables : List[str] = ["credentials", "profiles"]):
        assert self.connection is not None, "Database connection is not established"
        cursor = self.connection.cursor()
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                self.connection.commit()
                print(f"Table {table} dropped successfully")
            except Exception as error:
                self.connection.rollback()
                print(f"Error dropping table {table}: {error}")
        cursor.close()


if __name__ == "__main__":
    test = Database(
        host = os.getenv("TEST_DATABASE_HOST"),
        port = os.getenv("TEST_DATABASE_PORT"),
        username = os.getenv("TEST_DATABASE_USERNAME"),
        password = os.getenv("TEST_DATABASE_PASSWORD"),
        database = os.getenv("TEST_DATABASE_NAME")
    )

    test.migrate()
    test.drop()
    test.connection.close()