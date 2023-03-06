import logging, os
import config, db_utils
import keyboards, additional, sheet_util
from load_dotenv import load_dotenv
from jinja2 import Template
from datetime import timedelta, datetime
from pymongo import MongoClient
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram_calendar import simple_cal_callback, SimpleCalendar

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

root = 384860553

#Configure fsm_storage
storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)

class RegUserStatesGroups(StatesGroup):
    start = State()
    paswd = State()
    name = State()
    email = State()

class SaveLidStatesGroups(StatesGroup):
    logined = State()
    project = State()
    direction = State()
    city = State()
    name = State()
    phone = State()
    citizenship = State()
    source = State()
    date = State()
    time = State()



@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message):
    await message.answer(
        """Привет, это бот для работы. Для продолжения выбери один из вариантов""", reply_markup=keyboards.start_command_keyboard)
    await RegUserStatesGroups.start.set()

# @dp.message_handler(commands=['cancel'], state='*')
# async def send_welcome(message: types.Message):
#     await message.answer(
#         """Привет, это бот для работы. Для продолжения выбери один из вариантов""", reply_markup=keyboards.start_command_keyboard)
#     await RegUserStatesGroups.start.set()

@dp.message_handler(lambda message: message.text == 'Регистрация', state=RegUserStatesGroups.start)
async def user_registration(message: types.Message, state: FSMContext):
    if (db_utils.check_user(message.from_user.id)):
        await message.answer(f"Вы уже зарегистрированны! {db_utils.user_get_name(message.from_user.id)}", reply_markup=keyboards.work_keyboard)
        await state.finish()
        await SaveLidStatesGroups.logined.set()
    else:
        await message.answer("Введи пароль!")
        await RegUserStatesGroups.paswd.set()


@dp.message_handler(lambda message: message.text == 'Вход', state=RegUserStatesGroups.start)
async def user_login(message: types.Message):
    if (db_utils.check_user(message.from_user.id)):
        await message.answer(f"Добро пожаловать, {db_utils.user_get_name(message.from_user.id)}!", reply_markup=keyboards.work_keyboard)
        await SaveLidStatesGroups.logined.set()
    else:
        await message.answer("Не получилось, введи пароль!")
        await RegUserStatesGroups.paswd.set()

@dp.message_handler(content_types=['text'], state=RegUserStatesGroups.paswd,)
async def pass_check(message: types.Message, state: FSMContext):
    if(message.text == os.getenv('PASS')):
        await message.answer("Отлично! Давай знакомится, напиши мне свои ФИО:")
        await RegUserStatesGroups.next()


@dp.message_handler(content_types=['text'], state=RegUserStatesGroups.name,)
async def user_name_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date_reg'] = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')
        data['user_id'] = message.from_user.id
        data['name'] = message.text

    await message.answer("Теперь мне нужен твой email:")
    await RegUserStatesGroups.next()

@dp.message_handler(content_types=['text'], state=RegUserStatesGroups.email)
async def user_email_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text


    await message.answer(f"Поздравляю, {data['name']}, вы успешно зарегистрированы!", reply_markup=keyboards.work_keyboard)
    await state.finish()
    db_utils.save_user(data)
    await SaveLidStatesGroups.logined.set()

@dp.message_handler(lambda message: message.text == 'Сохранить лид', state=SaveLidStatesGroups.logined)
async def lid_add(message: types.Message):
    await message.answer('Выбери проект лида: ', reply_markup=keyboards.project_keyboard)
    await SaveLidStatesGroups.project.set()

@dp.message_handler(lambda message: message.text == 'Мой отчет', state=SaveLidStatesGroups.logined)
async def get_report(message: types.Message):
    await message.answer('Твой отчет начал формироваться надо чуток подождать)')
    await bot.send_message(message.from_user.id, 'Твой отчет доступен по ссылке:\n' + sheet_util.get_sheet(message.from_user.id))

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.project)
async def lid_project_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['date_reg'] = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')
        data['project'] = message.text

    await message.answer("Выбери направление лида: ", reply_markup=keyboards.direction_keyboard)
    await SaveLidStatesGroups.next()

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.direction)
async def lid_direction_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text

    await message.answer("Выбери город лида: ", reply_markup=keyboards.cities_keyboard)
    await SaveLidStatesGroups.next()

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.city)
async def lid_city_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

    await message.answer("Введи ФИО лида: ")
    await SaveLidStatesGroups.next()

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.name)
async def lid_name_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer("Введи телефон лида в формате\n9876543210: ")
    await SaveLidStatesGroups.next()

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.phone)
async def lid_phone_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.answer("Выбери гражданство лида: ", reply_markup=keyboards.citizenship_keyboard)
    await SaveLidStatesGroups.next()

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.citizenship)
async def lid_citizenship_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['citizenship'] = message.text

    await message.answer("Выбери источник лида: ", reply_markup=keyboards.source_keyboard)
    await SaveLidStatesGroups.next()

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.source)
async def lid_source_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['source'] = message.text

    await message.answer("Выбери дату собеседования лида: ", reply_markup=await SimpleCalendar().start_calendar())
    await SaveLidStatesGroups.next()

@dp.callback_query_handler(simple_cal_callback.filter(), state=SaveLidStatesGroups.date)
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Дата собеседования: {date.strftime("%d-%m-%Y")}'
        )
        async with state.proxy() as data:
            data['date'] = date.strftime('%d-%m-%Y')
        await bot.send_message(callback_query.from_user.id, "Выберите время собеседования лида: ", reply_markup=keyboards.time_keyboard)
        await SaveLidStatesGroups.next()

@dp.message_handler(content_types=['text'], state=SaveLidStatesGroups.time)
async def lid_time_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    ikb = types.InlineKeyboardMarkup()
    ikb1 = types.InlineKeyboardButton(text="Написать в WhatsApp", url=additional.get_whats_url(data))
    ikb.add(ikb1)
    db_utils.save_lid(data)
    await message.answer(additional.get_end_message(data), reply_markup=keyboards.work_keyboard)
    await bot.send_message(message.from_user.id, 'Вы можете сразу отправить сообщение этому лиду!', reply_markup=ikb)
    await SaveLidStatesGroups.logined.set()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)