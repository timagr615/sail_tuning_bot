from weather.weather_states import *
from bot import dp


@dp.message_handler(commands=['help', 'start'])
async def send_menu(message: Message):
    await message.reply(text='''Дступные команды:
    /help - подсказки по командам; \n
    /weather - узнать прогноз погоды для конкретного места \n''', reply=False)
