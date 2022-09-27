from variables import *
import re
from data.students import *
from data.events import Event
from data.companies import Company


def set_env_functions(real_bot):
    global bot
    bot = real_bot

def try_to_buy_merch(message, merch_name):
    student = Session.query(Student).get(message.chat.id)
    balance = int(student.balance)

    if student.merch_buy_ability_amt == 0:
            bot.send_message(message.chat.id, 'К сожалению, больше одной вещи купить нельзя', reply_markup=keyboard_back_menu)
    else:
        if merch_name.lower() == 'cup':
            if balance < cup_price:
                 bot.send_message(message.chat.id, 'У вас недостаточно коинов, чтобы купить это', reply_markup=keyboard_back_menu)
            else:
                student.balance -= cup_price
                student.merch_buy_ability_amt -= 1 
                student.bought_merch += f'<b>Невероятная HSE кружка 💥</b>\n'
                Session.commit()
                bot.send_message(message.chat.id, f'Поздравляю с покупкой, теперь у вас есть: \n{student.bought_merch}', parse_mode='HTML', reply_markup=keyboard_back_menu)
    
        elif merch_name.lower() == 'tshirtblack':
            if balance < tshirt_price:
                 bot.send_message(message.chat.id, 'У вас недостаточно коинов, чтобы купить это', reply_markup=keyboard_back_menu)
            else:
                student.balance -= tshirt_price
                student.merch_buy_ability_amt -= 1 
                student.bought_merch += f'<b>крутейшая HSE футболка 🔥</b>\n'
                Session.commit()
                bot.send_message(message.chat.id, f'Поздравляю с покупкой, теперь у вас есть \n{student.bought_merch}', parse_mode='HTML', reply_markup=keyboard_back_menu)
    
        elif merch_name.lower() == 'tshirtblue':
            if balance < tshirt_price:
                 bot.send_message(message.chat.id, 'У вас недостаточно коинов, чтобы купить это', reply_markup=keyboard_back_menu)
            else:
                student.balance -= tshirt_price
                student.merch_buy_ability_amt -= 1 
                student.bought_merch += f'<b>крутейшая HSE футболка 🔥</b>\n'
                Session.commit()
                bot.send_message(message.chat.id, f'Поздравляю с покупкой, теперь у вас есть \n{student.bought_merch}', parse_mode='HTML', reply_markup=keyboard_back_menu)
    
        elif merch_name.lower() == 'hudi':
            if balance < hudi_price:
                 bot.send_message(message.chat.id, 'У вас недостаточно коинов, чтобы купить это', reply_markup=keyboard_back_menu)
            else:
                student.balance -= hudi_price
                student.merch_buy_ability_amt -= 1
                student.bought_merch += f'<b>Неотразимый HSE свитшот 🌲</b>\n'
                Session.commit()
                bot.send_message(message.chat.id, f'Поздравляю с покупкой, теперь у вас есть \n{student.bought_merch}', parse_mode='HTML', reply_markup=keyboard_back_menu)
    
        elif merch_name.lower() == 'shopper':
            if balance < shoper_price:
                 bot.send_message(message.chat.id, 'У вас недостаточно коинов, чтобы купить это', reply_markup=keyboard_back_menu)
            else:
                student.balance -= shoper_price
                student.merch_buy_ability_amt -= 1 
                student.bought_merch += f'<b>Самый удобный HSE шоппер ☀</b>\n'
                Session.commit()
                bot.send_message(message.chat.id, f'Поздравляю с покупкой, теперь у вас есть \n{student.bought_merch}', parse_mode='HTML', reply_markup=keyboard_back_menu)
    
        elif merch_name.lower() == 'bottle':
            if balance < bottle_price:
                 bot.send_message(message.chat.id, 'У вас недостаточно коинов, чтобы купить это', reply_markup=keyboard_back_menu)
            else:
                student.balance -= bottle_price
                student.merch_buy_ability_amt -= 1 
                student.bought_merch += f'<b>крутейшая HSE бутылка 🔥</b>\n'
                Session.commit()
                bot.send_message(message.chat.id, f'Поздравляю с покупкой, теперь у вас есть \n{student.bought_merch}', parse_mode='HTML', reply_markup=keyboard_back_menu)
    
        elif merch_name.lower() == 'termocup':
            if balance < bottle_price:
                 bot.send_message(message.chat.id, 'У вас недостаточно коинов, чтобы купить это', reply_markup=keyboard_back_menu)
            else:
                student.balance -= bottle_price
                student.merch_buy_ability_amt -= 1 
                student.bought_merch += f'<b>крутейшая HSE термокружка 🔥</b>\n'
                Session.commit()
                bot.send_message(message.chat.id, f'Поздравляю с покупкой, теперь у вас есть \n{student.bought_merch}', parse_mode='HTML', reply_markup=keyboard_back_menu)
    

    update_phase(message, READY)
    return
   

def new_name(message):
    if message.text == 'Что ты хочешь изменить?':
        bot.send_message(message.chat.id, 'Введи корректные ФИО:')
        bot.register_next_step_handler(message, new_name)
        return
    if not check_name(message):
        bot.send_message(message.chat.id, 'Пожалуйста, введи ФИО еще раз в корректном формате!')
        bot.register_next_step_handler(message, new_name)
        return
    bot.send_message(message.chat.id, 'Данные успешно обновлены!', reply_markup=keyboard_back_menu)
    Session.query(Student).get(message.chat.id).fio = message.text
    Session.commit()
    update_phase(message, READY)


def new_email(message):
    if message.text == 'Что ты хочешь изменить?':
        bot.send_message(message.chat.id, 'Введи корректную электронную почту:')
        bot.register_next_step_handler(message, new_email)
        return
    if not check_email(message):
        bot.send_message(message.chat.id, 'Пожалуйста, введи корректную почту!')
        bot.register_next_step_handler(message, new_email)
        return
    Session.query(Student).get(message.chat.id).email = message.text
    update_phase(message, READY)
    Session.commit()
    bot.send_message(message.chat.id, 'Данные успешно обновлены!', reply_markup=keyboard_back_menu)


def update_students():
    students = Session.query(Student)
    students_dict = dict()
    for it in students:
        students_dict[it.chat_id] = it
    return students_dict


def update_promo_codes():
    stud = update_students()
    promo_codes = []
    for student in stud.values():
        promo_codes.append(student.promo_code)
    return promo_codes


def get_phase(message):
    student = Session.query(Student).get(message.chat.id)
    if student is None:
        return -1
    return student.phase


def update_phase(message, new_phase):
    student = Session.query(Student).get(message.chat.id)
    student.phase = new_phase
    Session.commit()


def update_wal1(message):
    stud = Session.query(Student).get(message.chat.id)
    stud.update_wal()


def check_email(message):
    if re.fullmatch(mail_pattern, message.text):
        return True
    return False


def check_name(message):
    if message.content_type != 'text':
        return False
    name = message.text
    return check_name_name(name)


def check_name_name(name):
    if not 2 <= len(name.split()) <= 3:
        return False
    for symb in name:
        if symb.isdigit():
            return False
    return True


def catalog():
    pass
    #Session.get(Catalog)

# спросить про оценку компаний
# def assess(message, stud):
#     bot.send_message(message.chat.id, 'Выбери компанию, вебинары которой тебе показались наиболее интересными:',
#                      reply_markup=get_kb_assess())
#
#
# def enter_coins(message, key, stud):
#     try:
#         coins = int(message.text)
#         if coins <= 0:
#             raise ValueError
#         if coins > stud.wal1:
#             raise ValueError
#     except ValueError:
#         bot.send_message(stud.chat_id, f'Ты можешь перевести компании от 1 до {stud.wal1} коинов, введи число еще раз:')
#         bot.register_next_step_handler(message, enter_coins, key, stud)
#         return
#     admit_coins(coins, key, stud)
#     bot.send_message(message.chat.id, 'Перевод успешно выполнен!')
#     check_if_assessed(message, stud)
#
#
# def check_if_assessed(message, stud):
#     if stud.wal1 > 0:
#         bot.send_message(stud.chat_id, f'Тебе нужно распределить еще {stud.wal1} {sklonenie_func(stud.wal1)}')
#         assess(message, stud)
#     else:
#         stud = Session.query(Student).get(stud.chat_id)
#         stud.assessed = True
#         Session.commit()
#         print(f'Студент {stud} распределил 10 % кошелька между компаниями.')
#         bot.send_message(stud.chat_id, f'Ты распределил свои коины между компаниями и теперь можешь обменять'
#                                        f' основную сумму счета ({stud.balance} {sklonenie_func(stud.balance)}) на мерч!\n'
#                                        f'Переходи по ссылке и оформляй заказ!\nhttps://docs.google.com/forms/d/e/1FAIpQLSdocdxJaXBGHGDhcssgJoip1WiuTZ5SjiV--82mjxssw2fkLw/viewform\n'
#                                        f'Спасибо за участие в Неделе Карьеры :)')
#
#
# def admit_coins(coins, key, stud):
#     company = Session.query(Company).filter(Company.name == key).one()
#     company.balance += coins
#     stud = Session.query(Student).get(stud.chat_id)
#     stud.wal1 -= coins
#     stud.balance -= coins
#     print(f'{stud} начислил компании {company.name} {coins} коинов')
#     Session.commit()
