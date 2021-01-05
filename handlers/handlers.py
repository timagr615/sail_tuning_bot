from weather.weather_states import *
from tuning.tuning_states import *
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
