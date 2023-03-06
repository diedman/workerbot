from jinja2 import Template
import urllib.parse

cities = ['Москва',
          'Санкт-Петербург',
          'Калининград',
          'Великий Новгород',
          'Курск',
          'Орел',
          'Тула',
          'Смоленск']

paymatka = {
    'Москва': 'https://eda.yandex/rabota/courier/pamyatka/msk',
    'Санкт-Петербург': 'https://eda.yandex/rabota/courier/pamyatka/spb',
    'Калининград': 'https://eda.yandex/rabota/courier/pamyatka/partner_klg',
    'Великий Новгород': 'https://eda.yandex/rabota/courier/pamyatka/v_novgorod',
    'Курск': 'https://eda.yandex/rabota/courier/pamyatka/kursk',
    'Орел': 'https://eda.yandex/rabota/courier/pamyatka/orel',
    'Тула': 'https://eda.yandex/rabota/courier/pamyatka/partner_tula',
    'Смоленск': 'https://eda.yandex/rabota/courier/pamyatka/smolensk',
}

addresses = {
    'Москва': 'г. Москва, Огородный проезд, д. 12. \nОфис работает каждый день с 9:30 - 19:30',
    'Санкт-Петербург': 'г. Санкт-Петербург, Заневский пр-т., д. 65, к 5. (ТЦ «Платформа», 5 этаж). \nОфис работает каждый день с 9:30 - 19:30',
    'Калининград': 'г. Калининград, ул. Генерал-лейтенанта Озерова 19, корпус 2. \nОфис работает ПН, ВТ, ПТ 12:00 - 16:00',
    'Великий Новгород': 'г. Великий Новгород, Александра Корсунова проспект, 28а, второй этаж офис 27/2. \nОфис работает ВТ, ЧТ 11:00 - 17:00',
    'Курск': 'г. Курск, пр-т Хрущева, д. 24. \nОфис работает ПН - ПТ 12:00 - 16:00',
    'Орел': 'г. Орел, ул.Веселая, д. 2. \nОфис работает ПН- ПТ 10:00 - 16:00',
    'Тула': 'г. Тула, ул. Макса Смирнова, д. 2, офис 6. \nОфис работает ПН - ПТ 10:00 - 16:00',
    'Смоленск': 'г. Смоленск, ул. Герцена, д.3, оф. 2. \nОфис работает ПН - ПТ 10:00 - 16:00'
}

documents = {
'rf': '''- Паспорт;
- СНИЛС ( можно фото )
- ИНН ( можно фото )
- Реквизиты личной банковской карты''',
'nrf': '''— Паспорт (со всеми штампами пересечений)
— Регистрация
— Патент: должность курьер, разнорабочий, либо без должности (с двух сторон)
— Чеки об оплате патента (можно электронные)
— ДМС
— Миграционная карта - цель въезда "работа"
— Реквизиты банковской карты - Сбербанк (если нет, то партнёр поможет с оформлением )
— СНИЛС
'''}

citizenships = ['РФ', 'ЕАЭС', 'Не РФ']

sources = ['HH', 'Авито', 'Юла', 'Работа.ру']

times = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']

def get_whats_message(data):
    if (data['citizenship'] == 'РФ'):
        document = documents['rf']
    else:
        document = documents['nrf']

    message = (
        f"""
        Добрый день.
Ждём Вас в офисе
на активацию {data['project']} ({data['direction']})
*{data['date']} в {data['time']}*

*Адрес офиса {data['city']}:*
{addresses[data['city']]}

Памятка, как пройти до офиса:
{paymatka[data['city']]}

*Подготовьте пакет документов*
{document}
        """
    )
    return message


def get_end_message(data):
    end_message = (f"""
*{data['direction']} успешно зарегестрирован!!*

*ФИО курьера:*
{data['name']}

*Номер телефона:*
{data['phone']}

*Город:*
{data['city']}

*Гражданство:*
{data['citizenship']}

*Источник трафика:*
{data['source']}

*Дата и время собеседования:*
{data['date']} {data['time']} ({data['project']})
""")
    return end_message

def get_whats_url(data):
    message = get_whats_message(data)
    string = urllib.parse.quote(message)
    phone = '+7' + data['phone']
    url = 'https://api.whatsapp.com/send/?phone='+phone+'&text='+string
    return url