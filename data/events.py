from sqlalchemy import Column, Integer, String
from data.database import Base


class Event(Base):
    __tablename__ = 'events'

    number = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(String)
    description = Column(String)
    link = Column(String)

    def __init__(self, number: int, name: str, datetime: str, description: str, link: str):
        self.number = number
        self.name = name
        self.datetime = datetime
        self.description = description
        self.link = link

    def __repr__(self):
        return f'Вебинар №{self.id}, название: {self.name}, ссылка: {self.balance}'