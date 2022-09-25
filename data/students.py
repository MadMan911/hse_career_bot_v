from sqlalchemy import Column, Integer, String, BOOLEAN
from data.database import Base
import random
from variables import *


def generate_code(length=8):
    alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    code = ''
    for _ in range(length):
        code += alphabet[random.randint(0, len(alphabet) - 1)]
    return code


class Student(Base):
    __tablename__ = 'students'

    chat_id = Column(Integer, primary_key=True)    #primary_key => первичный ключ
    fio = Column(String)
    user_name = Column(String)
    email = Column(String)
    balance = Column(Integer)
    wal1 = Column(Integer)
    phase = Column(Integer)
    promo_code = Column(String)
    activations = Column(Integer)
    entered_promo_code = Column(BOOLEAN)
    assessed = Column(BOOLEAN)
    order = Column(Integer)


    def __init__(self, chat_id: int, fio: str, user_name: str, email=''):
        self.chat_id = chat_id
        self.fio = fio
        self.user_name = user_name
        self.email = email
        self.balance = default_balance
        self.wal1 = 0
        self.phase = REG
        self.promo_code = generate_code()
        self.activations = 0
        self.entered_promo_code = False
        self.assessed = False
        self.order = None

    def update_wal(self):  #10 процентов счета, метод вызывается, когда поользователь переходит к оценке компаний
        self.wal1 = int(0.1 * self.balance)
        if self.wal1 == 0:
            self.wal1 = 1

    def sklonenie(self):
        numb = self.balance % 100
        if numb == 1 or numb % 10 == 1:
            return 'коин'
        if 2 <= numb <= 4 or 2 <= numb % 10 <= 4:
            return "коина"
        if 5 <= numb <= 20 or numb % 10 != 1:
            return 'коинов'

    def get_balance(self):
        return f'Твой баланс составляет {self.balance} {self.sklonenie()}. Чтобы заработать больше, участвуй ' \
               f'в вебинарах, проявляй активность, ' \
               f'а также приглашай друзей участвовать в Неделе Карьеры! Если твой друг активирует промокод, выданный ' \
               f'тебе в начале регистрации ({self.promo_code}), то вы оба получите по 5 коинов :)'

    def get_balance_light(self):
        return f'{self.balance} {self.sklonenie()}'

    def __repr__(self):
        return f'cтудент {self.fio}, chat_id: {self.chat_id}, почта: {self.email}, баланс: {self.balance}, ' \
               f'применил ли промокод: {"Да" if self.entered_promo_code else "Нет"}, ' \
               f'выданный промокод: {self.promo_code}, фаза: {self.phase}'

    def change_fio(self, new_fio):
        self.fio = new_fio

    def wallets(self):
        self.update_wal()
        wal2 = self.balance - self.wal1
        return f'Необходимо *распределить между компаниями:* {self.wal1} {sklonenie_func(self.wal1)}\n' \
               f'Затем можно потратить на *мерч:* {wal2}' \
               f' {sklonenie_func(wal2)}'


def sklonenie_func(number):
    numb = number % 100
    if numb % 10 == 1 and numb != 11:
        return 'коин'
    if 2 <= numb <= 4 or 2 <= numb % 10 <= 4:
        return "коина"
    else:
        return 'коинов'

