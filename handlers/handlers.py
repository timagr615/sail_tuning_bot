from weather.weather_states import *
from tuning.tuning_states import *
from personal_tuning.personal_tuning_states import *
from personal_tuning.personal_show_states import *
from bot import dp
from db import crud
from db.database import SessionLocal
from config import ADMIN_ID


@dp.message_handler(commands=['help', 'start'])
async def send_menu(message: Message):
    db = SessionLocal()
    crud.create_user(db, message)
    db.close()
    await message.reply(text='''Дступные команды:
    /help - подсказки по командам; \n
    /tuning - выбрать настройку; \n
    /create - записать личную настройку; \n
    /show - показать личные настройки; \n
    /weather - узнать прогноз погоды для конкретного места \n''', reply=False)


@dp.message_handler(commands=['users'])
async def get_users(message: Message):
    if message['from'].id == ADMIN_ID:
        db = SessionLocal()
        users = crud.get_users(db)
        db.close()
        text = ''
        for user in users:
            text += 'id: ' + str(user.telegram_id) + '\n' + user.firstname + ' ' + user.lastname + '\n' + '\n'
        await message.answer(text=text)
    else:
        await message.answer(text='Команда доступна только для администраторов')


@dp.message_handler()
async def process_help(message: Message):
    await message.answer(
        '/help - помощь по доступным командам.'
    )
