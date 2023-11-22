from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    __table_args__ = {'schema': 'traning'}

    id = Column('id', Integer, nullable=False, primary_key=True)
    name = Column('name', String, nullable=False)
    joined_time = Column('joined_time', TIMESTAMP, nullable=False,server_default=func.now(), onupdate=func.now())
