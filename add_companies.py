from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.companies import Company

engine = create_engine(f'postgresql://wehgyhaiftwaip:f07b877cd0d5cc5845a663e9b55dcbc78aa66794ce9b43920fa8f9ef9f3fe3f7@ec2-54-171-25-232.eu-west-1.compute.amazonaws.com:5432/d7acfhm3rlibk9')
session = sessionmaker(bind=engine)
Session = session()


coms = [
    Company(
        id=1,
        name='1C',
        description='Компания:1C\n\nСпикер - Старичков Никита , заместитель директора по работе с НИУ   \n\nТема : "Перспективы карьеры в 1С"\n\n Время: 14:15 03.10.2022 \n\n Cсылка: https://events.webinar.ru/gsbhse/1901547011',
        balance=0,
    ),
    Company(
        id=2,
        name='КРОК',
        description='Компания:KPOK\n\nСпикер - Юлия Сашникова, тимлид команды по развитию бренда работодателя КРОК \n\nТема " Старт карьеры в КРОКе"  \n\n15:30 03.10.2022\n\nСсылка: https://events.webinar.ru/gsbhse/760511788',
        balance=0,
    ),
    Company(
        id=3,
        name='Центр карьеры ВШБ',
        description='омпания: Центр карьеры ВШБ \n\nСпикер Екатерина Сабитова - рекрутёр с 10 летним опытом, член  \n\nТема : «Разбор ошибок при поиске работы. Карьерные лайфхаки». \n\nВремя:16:45 03.10.2022 \n\nСсылка: https://events.webinar.ru/gsbhse/104254475',
        balance=0,
    ),
    Company(
        id=4,
        name='X5 Retail Group (много лосося)',
        description='Компания: Х5 Retail Group (Много лосося ) \n\nСпикер: Александр Чернов - Х5 Retail Group (Много лосося ), директор управления информационных технологий, выпускник бак БИ 2018, маг Системы больших данных 2020 \n\n Тема : «"Успешные карьерные траектории выпускников ВШБ: Опыт работы в компании Х5 Retail Group» \n\nВремя:  18:00 03.10.2022\n\nСсылка: https://events.webinar.ru/gsbhse/538780903',
        balance=0,
    ),
    Company(
        id=5,
        name='СКОЛТЕХ',
        description='Компания: СКОЛТЕХ \n\n Спикер - Денис Столяров, Проректор по работе со студентами  \n\n Тема "Карьера в науке" \n\nВремя: 14:15 04.10.2022 \n\nСсылка:https://events.webinar.ru/gsbhse/1611850438',
        balance=0,
    ),
    Company(
        id=6,
        name='ЭКОПСИ',
        description='Компания: ЭКОПСИ \n\n Марина Баранова, член правления и директор по развитию бизнеса \n\n Тема "Мифы и реальность консалтинга: решая проблемы большого бизнеса"\n\nВремя: 15:30 04.10.2022 \n\nСсылка:https://events.webinar.ru/gsbhse/423468793',
        balance=0,
    ),
    Company(
        id=7,
        name='Росэнергоатом',
        description='Компания: Росэнергоатом    \n\n Спикер - Ильина Елена , директор по вопросам государственной поддержки, выпускница бак Управление  Бизнесом 2012; маг 2014 Маркетинговые коммуникации   \n\n Тема: " Успешные карьерные траектории выпускников ВШБ: Опыт работы в компании Росатом. " \n\nВремя: 14:15 06.10.2022 \n\nСсылка: https://events.webinar.ru/gsbhse/1400062895',
        balance=0,
    ),
    Company(
        id=8,
        name='VK',
        description='Компания: VK \n\n Евгения Евтеева, руководитель направления студенческих проектов \n\n Тема «Как начать карьеру в IT и подготовится к собеседованиям в турбулентное время» \n\nВремя: 15:30 06.10.2022 \n\nСсылка:https://events.webinar.ru/gsbhse/2013069928',
        balance=0,
    ),
    Company(
        id=9,
        name='Сбер',
        description='Компания: СБЕР \n\n Спикер - Ирина Арзуманян, Руководитель направления, Дирекция академических партнерств Сбер \n\n Тема: «О Сбере и карьере в Сбере» \n\nВремя: 16:45 06.10.2022 \n\nСсылка: https://events.webinar.ru/gsbhse/1666701507',
        balance=0,
    ),
    Company(
        id=10,
        name='АксТим (AxTeam) (Accenture)',
        description='Компания: АксТим (AxTeam) (Accenture) \n\n Спикер - Алексей Курочкин, Program & Project Manager \n\n Тема  :"Новые вызовы консалтинга"  \n\nВремя: 18:00 06.10.2022 \n\nСсылка: https://events.webinar.ru/gsbhse/1001674067',
        balance=0,
    )
]


for com in coms:
    Session.add(com)

Session.commit()

