import os, sys

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session
from datetime import date

from src.adapters.context import Context
from src.domain.models import Credentials, Profile
from src.auth.criptography import Cryptography

if __name__ == '__main__':
    database_url = URL.create(
        drivername="postgresql",
        username="ericcar",
        password="eric1997",
        host="localhost",
        port="5432",
        database="auth_tests"
    )

    engine = create_engine(database_url)
    session_factory = sessionmaker(bind=engine) 
    context = Context(session_factory)
    context.cryptography = Cryptography()

    with context as context:
        context.users.add_user(
            Credentials(
                username="ericcar",
                email="eric.m.cardozo@gmail.com",
                password=context.cryptography.hash("password")
            ),

            Profile(
                first_name="Eric",
                last_name="Cardozo",
                birthdate=date(1997, 9, 30)
            )
        )

        context.commit()
        user = context.users.get_user_by_username("ericcar")
        print(user.id)

        context.users.remove_user_by_username("ericcar")
        context.commit()