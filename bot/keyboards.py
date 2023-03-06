from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from additional import cities, citizenships, sources, times
import datetime

remove = ReplyKeyboardRemove()

start_command_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_command_keyboard.add('Регистрация', 'Вход')

work_keyboard = ReplyKeyboardMarkup(True, True)
work_keyboard.add('Мой отчет', 'Сохранить лид')

project_keyboard = ReplyKeyboardMarkup(True, True)
project_keyboard.add('Яндекс.Еда', 'Яндекс.Лавка', 'Delivery Club')

direction_keyboard = ReplyKeyboardMarkup(True, True)
direction_keyboard.add('Пеший курьер', 'Автокурьер')

cities_keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True,  row_width=2)
for i in range(0, len(cities), 2):
    cities_keyboard.row(cities[i], cities[i+1])

citizenship_keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True, row_width=2)
for i in range(0, len(citizenships)):
    citizenship_keyboard.add(KeyboardButton(citizenships[i]))

source_keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True, row_width=2)
for i in range(0, len(sources), 2):
    source_keyboard.row(sources[i], sources[i+1])

time_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in range(0, len(times)):
    time_keyboard.add(KeyboardButton(times[i]))
