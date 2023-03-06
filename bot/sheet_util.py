import pandas as pd
import gspread, config, os
from datetime import datetime
from pymongo import MongoClient

# Подключение к базе данных MongoDB
client = MongoClient(config.mongodbip, config.mongodbport)
db = client['users_db']
lid_collection = db['lid_collection']
user_collection = db['users_collection']
gc = gspread.service_account(filename=os.getcwd() + '/bot/services.json')

def del_all_sheet():
    sheets = gc.list_spreadsheet_files()
    for i in sheets:
        gc.del_spreadsheet(i['id'])

def get_sheet(user_id):

    date = datetime.now().strftime("%d-%m-%Y")

    user = user_collection.find_one({'user_id': user_id})
    user_email = user['email']

    columns = ['Дата регистрации', 'Проект', 'Направление', 'Город', 'ФИО', 'Телефон', 'Гражданство', 'Источник', 'Дата собеседования', 'Время собеседования']

    # Получение данных из коллекции MongoDB в виде DataFrame
    data = pd.DataFrame(list(lid_collection.find({'user_id': user_id}, {'_id': False, 'user_id': False})))
    print(data)

    #Создание документа и его открытие
    sh = gc.create(date)
    sh = gc.open(date)

    #Получение первого листа документа
    worksheet = sh.get_worksheet(0)

    #Запись данных из БД построчно
    for values in data.values:
        worksheet.insert_row(values.tolist())

    #Шапка
    worksheet.insert_row(columns)

    #Пердоставление доступа
    sh.share(user_email, perm_type='user', role='writer')
    #Ссылка
    return "https://docs.google.com/spreadsheets/d/%s" % sh.id

