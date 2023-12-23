from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AccountSchema(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable = False, unique = True)
    password = Column(String(100), nullable = False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(user_id={self.id}, username={self.username})>"
    