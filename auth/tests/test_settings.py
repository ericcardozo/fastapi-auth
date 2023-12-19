import os, dotenv
from sqlalchemy import URL, create_engine
from src.domain.settings import Settings

dotenv.load_dotenv()

TEST_SETTINGS = Settings(
    database_url = URL.create(
        drivername=os.getenv("TEST_DATABASE_DRIVERNAME"),
        username=os.getenv("TEST_DATABASE_USERNAME"),
        password=os.getenv("TEST_DATABASE_PASSWORD"),
        host=os.getenv("TEST_DATABASE_HOST"),
        port=os.getenv("TEST_DATABASE_PORT"),
        database=os.getenv("TEST_DATABASE_NAME")
    )
)

