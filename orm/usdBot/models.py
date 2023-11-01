from sqlalchemy import Column, VARCHAR, Integer, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()

class Users(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    user_id = Column(VARCHAR(50), unique = True)
    notifications = Column(Boolean)
