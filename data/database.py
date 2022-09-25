from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data.config import DATABASE_NAME
# from data.events import Event
# from data.students import Student
# from data.companies import Company


engine = create_engine(f'postgresql://wehgyhaiftwaip:f07b877cd0d5cc5845a663e9b55dcbc78aa66794ce9b43920fa8f9ef9f3fe3f7@ec2-54-171-25-232.eu-west-1.compute.amazonaws.com:5432/d7acfhm3rlibk9')
# connect_args={'check_same_thread': False}
session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
