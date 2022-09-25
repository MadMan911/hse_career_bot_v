import telebot
from data.config import *
from functions import *
from variables import *
import os
from data.database import DATABASE_NAME
import traceback
from create_database import create_database
from data.students import Student


bot = telebot.TeleBot(TOKEN)


@bot.callback_query_handler(func=lambda call: call.data == 'go_to_final')
def go_to_final(call):
    student = Session.query(Student).get(call.message.chat.id)
    # update_phase(call.message, READY)
    if get_phase(call.message) > 2:
        update_phase(call.message, READY_2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'{call.message.text}', reply_markup=None)
        bot.send_message(call.message.chat.id, final_intro)
        bot.send_message(call.message.chat.id, f'Твой баланс составляет {student.get_balance_light()}.\n'
                                               f'{student.wallets()}',
                         reply_markup=keyboard_final, parse_mode='MarkDown')


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == -1)
def handle_none_type(call):
    bot.send_message(call.message.chat.id, 'Произошла ошибка, нужно еще раз зарегистрироваться... Пожалуйста, введи '
                                           'ФИО:')
    bot.register_next_step_handler(call.message, reg_name)


@bot.message_handler(func=lambda message: get_phase(message) == -1)
def handle_none_type(message):
    bot.send_message(message.chat.id, 'Произошла ошибка, нужно еще раз зарегистрироваться... Пожалуйста, введи '
                                           'ФИО:')
    print(message.chat.id)
    bot.register_next_step_handler(message, reg_name)


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in update_students().keys():
        bot.send_message(message.chat.id, 'Ты уже зарегистрировался! Хочешь внести изменения в свой профиль?',
                         reply_markup=keyboard_changes)
        update_phase(message, CHANGE_REG_1)
        return
    bot.send_message(message.chat.id, welcome, parse_mode='HTML')
    print(f'Пользователь {message.from_user.username} запустил бота')
    bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    if not check_name(message):
        bot.send_message(message.chat.id, 'Пожалуйста, введи ФИО еще раз в корректном формате!')
        bot.register_next_step_handler(message, reg_name)
        return
    fio = message.text
    new_student = Student(message.chat.id, fio, message.from_user.username)
    Session.add(new_student)
    bot.send_message(message.chat.id, 'Теперь введи электронную почту, с которой будешь регистрироваться'
                                      ' на вебинары Недели Карьеры:')
    bot.register_next_step_handler(message, reg_email)


@bot.message_handler(func=lambda message: get_phase(message) == REG)
def reg_email(message):
    if not check_email(message):
        bot.send_message(message.chat.id, 'Пожалуйста, введи корректную почту! Если ты студент ВШЭ,'
                                          ' предпочтительно использовать корпоративную почту.')
        bot.register_next_step_handler(message, reg_email)
        return
    bot.send_message(message.chat.id, about_coins)
    Session.query(Student).get(message.chat.id).email = message.text
    print(f'Зарегистрирован: {Session.query(Student).get(message.chat.id)}')
    update_phase(message, GIVE_PROMO)
    bot.send_message(message.chat.id, 'У тебя есть промокод от других участников Недели Карьеры? При его активации ты '
                                      'получишь 5 коинов.',
                     reply_markup=keyboard_promo)


def activate_promo(message):
    if get_phase(message) != ENTER_PROMO:
        update_phase(message, READY)
        bot.register_next_step_handler(message, menu)
        return
    code = message.text
    if code not in update_promo_codes():
        if code == 'menu' or code == 'Меню':
            return
        bot.send_message(message.chat.id, 'Введенный промокод недействителен! Попробуй ввести другой',
                         reply_markup=keyboard_back)
        bot.register_next_step_handler(message, activate_promo)
    elif code == Session.query(Student).get(message.chat.id).promo_code:
        bot.send_message(message.chat.id, 'Ты не можешь активировать промокод, выданный тебе :(',
                         reply_markup=keyboard_back)
    else:
        notify = Session.query(Student).filter(Student.promo_code == message.text).first()
        if notify.activations == 5:
            bot.send_message(message.chat.id, 'Этот промокод применили уже 5 раз, больше нельзя :(',
                             reply_markup=keyboard_back)
            return
        bot.send_message(notify.chat_id, 'Другой пользователь активировал твой промокод! На твой счет зачислено '
                                         '5 коинов :)', reply_markup=keyboard_menu)
        notify.activations += 1
        notify.balance += 5
        Session.query(Student).get(message.chat.id).balance += 5
        Session.query(Student).get(message.chat.id).entered_promo_code = True
        bot.send_message(message.chat.id, 'Промокод успешно активирован! На твой счет зачислено 5 коинов',
                         reply_markup=keyboard_menu)
        update_phase(message, READY)


@bot.message_handler(func=lambda message: get_phase(message) == GIVE_PROMO)
def new_promo(message):
    bot.send_message(message.chat.id, f'Ты успешно зарегистрирован! Вот твой уникальный промокод. Если другой '
                                      f'участник Недели Карьеры при регистрации его '
                                      f' активирует, ты получишь 5 коинов.\nПриглашай друзей участвовать в '
                                      f'осенней Неделе Карьеры ВШБ! Промокод действителен на 5 применений:')
    bot.send_message(message.chat.id, f'*{Session.query(Student).get(message.chat.id).promo_code}*',
                     parse_mode="Markdown", reply_markup=keyboard_back_menu)
    update_phase(message, READY)


@bot.message_handler(func=lambda message: get_phase(message) == READY)
def handle_wrong_text(message):
    bot.send_message(message.chat.id, 'Пожалуйста, воспользуйся кнопками ниже!')
    menu(message)


@bot.message_handler(func=lambda message: message.text == 'Меню')
def menu(message):
    try:
        if Session.query(Student).get(message.chat.id).entered_promo_code:
            bot.send_message(message.chat.id, 'Выбери пункт меню:', reply_markup=keyboard_menu_light)
        else:
            bot.send_message(message.chat.id, 'Выбери пункт меню:', reply_markup=keyboard_menu)
    except AttributeError:
        bot.send_message(message.chat.id, 'Выбери пункт меню:', reply_markup=keyboard_menu)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == GIVE_PROMO or call.data == 'activate_promo')
def is_promo_needed(call):
    if Session.query(Student).get(call.message.chat.id).entered_promo_code:
        bot.send_message(call.message.chat.id, 'Ты уже активировал промокод!', reply_markup=keyboard_back)
        return
    if call.data == 'activate_promo':
        bot.send_message(call.message.chat.id, 'Введи промокод другого участника Недели Карьеры:',
                         reply_markup=keyboard_back)
        update_phase(call.message, ENTER_PROMO)
        bot.register_next_step_handler(call.message, activate_promo)
    elif call.data == 'skip_activate_promo':
        new_promo(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def handle_back(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.message.text}',
                          reply_markup=None, parse_mode="Markdown")
    update_phase(call.message, READY)
    menu(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == READY)
def handle_menu(call):
    if call.data == 'event_calendar':
        bot.send_message(call.message.chat.id, event_calendar_str(), parse_mode="Markdown", reply_markup=keyboard_back)
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} посмотрел календарь')
    elif call.data == 'rules':
        bot.send_message(call.message.chat.id, rules, reply_markup=keyboard_back, parse_mode='MarkDown')
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} посмотрел правила игры')
    elif call.data == 'companies':
        bot.send_message(call.message.chat.id, 'Вот список компаний, сотрудничающих с ВШБ на осенней Неделе Карьеры. '
                                               'Нажмите на кнопку, чтобы почитать про компанию подробнее. ',
                         reply_markup=get_kb_companies())
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} посмотрел список компаний')
    elif call.data == 'balance':
        ans = Session.query(Student).get(call.message.chat.id).get_balance()
        bot.send_message(call.message.chat.id, ans, reply_markup=keyboard_back)
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} посмотрел свой баланс')
    elif call.data == 'info':
        bot.send_message(call.message.chat.id, info, reply_markup=keyboard_back, parse_mode='HTML')
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} посмотрел информацию о НК')
    elif call.data in companies_dict().keys():
        comp = companies_dict()
        for key, val in comp.items():
            if call.data == key:
                bot.send_message(call.message.chat.id, val, reply_markup=keyboard_back)
                print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} посмотрел информацию о '
                      f'компании {key}')
                break
    elif call.data == 'change_reg':
        bot.send_message(call.message.chat.id, f"Данные твоего профиля сейчас:\n\n"
                                               f"Твои ФИО:\n*{Session.query(Student).get(call.message.chat.id).fio}*\n\n"
                                               f"Твоя электронная почта:\n*{Session.query(Student).get(call.message.chat.id).email}*"
                                               f"\n\nОбрати внимание, что твоя почта должна совпадать с той, с которой "
                                               f"ты будешь регистрироваться на вебинары Недели Карьеры. В противном "
                                               f"случае мы не сможем начислить тебе коины :(", parse_mode='MarkDown')
        bot.send_message(call.message.chat.id, 'Ты хочешь отредактировать свой профиль?',
                         reply_markup=keyboard_changes)
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} просмотрел свой профиль')
        update_phase(call.message, CHANGE_REG_1)
    else:
        bot.send_message(call.message.chat.id, 'Пожалуйста, воспользуйтесь кнопками меню:')
        print(call.message.chat.id)
        menu(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == CHANGE_REG_1)
def check_reg(call):
    if call.data == 'changes_needed':
        update_phase(call.message, CHANGE_REG_2)
        bot.send_message(call.message.chat.id, 'Что ты хочешь изменить?', reply_markup=keyboard_change_reg)
    elif call.data == 'no_changes_needed':
        update_phase(call.message, READY)
        bot.send_message(call.message.chat.id, 'Изменения не внесены.', reply_markup=keyboard_back_menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.message.text}',
                          reply_markup=None, parse_mode="Markdown")
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == CHANGE_REG_2)
def change_reg(call):
    if call.data == 'change_fio':
        new_name(call.message)
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} изменил ФИО')
    elif call.data == 'change_email':
        new_email(call.message)
        print(f'Пользователь {Session.query(Student).get(call.message.chat.id)} изменил свою почту')
    bot.answer_callback_query(callback_query_id=call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.message.text}',
                          reply_markup=None, parse_mode="Markdown")


@bot.message_handler(
    content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                   "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                   "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                   "migrate_from_chat_id", "pinned_message"])
def send_sticker(message):
    sticker = open('./sticker_hse.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == READY_2)
def assess_or_merch(call):
    if call.data == 'assess':
        update_phase(call.message, ASSESS)
        update_wal1(call.message)
        print(f'{Session.query(Student).get(call.message.chat.id)} перешел к оценкам компаний')
        assess(call.message, None)
    bot.answer_callback_query(callback_query_id=call.id)
    # elif call.data == 'catalog':
    #     catalog(call.message)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == ASSESS)
def assess_1(call):
    companies = companies_dict()
    stud = Session.query(Student).get(call.message.chat.id)
    for key in companies.keys():
        if key == call.data:
            bot.send_message(call.message.chat.id, 'Сколько коинов ты хочешь перевести выбранной компании?')
            bot.register_next_step_handler(call.message, enter_coins, key, stud)
            bot.answer_callback_query(callback_query_id=call.id)
            return


if __name__ == '__main__':
    set_env_functions(bot)
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_database()
    print('Бот успешно запущен')
    while True:
        try:
            Session.rollback()
            bot.infinity_polling(timeout=None)
        except Exception as e:
            import time
            traceback.print_exc()
            bot.send_message(426184690, traceback.format_exc()) # отпарвку мне сдеалть
            del bot
            bot = telebot.TeleBot(real)
            Session.rollback()
            time.sleep(5)
            
