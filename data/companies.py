from sqlalchemy import Column, Integer, String
from data.database import Base


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)    # primary_key => первичный ключ
    description = Column(String)
    balance = Column(Integer)

    def __init__(self, id: int, name: str, description: str, balance: int):
        self.id = id
        self.name = name
        self.description = description
        self.balance = balance

    def __repr__(self):
        return f'Компания №{self.id}, название: {self.name}, баланс: {self.balance}'