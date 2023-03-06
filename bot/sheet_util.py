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

def create_sheet(user_id):
    columns = ['Дата регистрации', 'Проект', 'Направление', 'Город', 'ФИО', 'Телефон', 'Гражданство', 'Источник', 'Дата собеседования', 'Время собеседования','Написать в WhastApp', 'Комментарий', 'Статус']
    user = user_collection.find_one({'user_id': user_id})
    sh = gc.create(user['name'])
    wh = sh.get_worksheet(0)
    wh.insert_row(columns)
    sh.share(user['email'], perm_type='user', role='writer')

def update_sheet(user_id):
    user = user_collection.find_one({'user_id': user_id})
    user_lid = lid_collection.find({'user_id': user_id, 'sheet': False}, {'_id': False, 'user_id': False, 'sheet': False})
    data = pd.DataFrame(list(user_lid))
    sh = gc.open(user['name'])
    worksheet = sh.get_worksheet(0)
    for values in data.values:
        worksheet.insert_row(values.tolist(), 2, value_input_option='USER_ENTERED')
    lid_collection.update_many(
        {
            'user_id': user_id,
            'sheet': False
        },
        {
            '$set' : {'sheet': True}
        })
    return "https://docs.google.com/spreadsheets/d/%s" % sh.id