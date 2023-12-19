from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable = False, unique = True)
    email = Column(String(100), nullable = False, unique = True)
    password = Column(String(100), nullable = False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(user_id={self.id}, username={self.username}, email={self.email})>"
    

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, ForeignKey('credentials'), primary_key = True)
    first_name = Column(String(50), nullable = False)
    last_name = Column(String(50), nullable = False)
    birthdate = Column(Date)

    def __repr__(self):
        return f'<UserProfile(user_id{self.id}, name={self.first_name} {self.last_name})>'