from pymongo import MongoClient
import config

global db
client = MongoClient(config.mongodbip, config.mongodbport)
db = client.users_db
phone_code = '+7'
# Проверка наличия пользователя в БД
def check_user(user_id):
    collection = db['users_collection']
    exists = collection.count_documents({ 'user_id': user_id }) == 1
    return exists

def user_get_name(user_id):
    collection = db['users_collection']
    exists = collection.find_one({ 'user_id': user_id })
    return exists['name']

def save_user(data):
    collection = db['users_collection']
    collection.insert_one({
        'date_reg': data['date_reg'],
        'user_id': data['user_id'],
        'name': data['name'],
        'email': data['email']
    })

def save_lid(data):
    collection = db['lid_collection']
    collection.insert_one({
        'date_reg': data['date_reg'],
        'user_id': data['user_id'],
        'project': data['project'],
        'direction': data['direction'],
        'city': data['city'],
        'name': data['name'],
        'phone': data['phone'],
        'citizenship': data['citizenship'],
        'source': data['source'],
        'date_interview': data['date'],
        'time_interview': data['time']
    })




