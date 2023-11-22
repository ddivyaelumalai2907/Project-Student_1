from sqlalchemy import Column, BigInteger, Integer, SmallInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class StudentSubject(Base):
    __tablename__ = 'student_subject'
    __table_args__ = {'schema': 'traning'}

    id = Column('id', BigInteger, nullable=False, primary_key=True)
    student_id = Column('student_id', Integer, nullable=False)
    subject_id = Column('subject_id', SmallInteger, nullable=False)
    subscription_time = Column('subscription_time', TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
