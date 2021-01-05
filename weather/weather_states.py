from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from bot import dp, weather
from aiogram.dispatcher import FSMContext
from .weather_app import current_weather_format
from config import logger


class Weather(StatesGroup):
    location = State()


@dp.message_handler(commands='weather')
async def weather_start(message: Message):
    await Weather.location.set()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Укажите геолокацию и мы вычислим прогноз погоды.", request_location=True))
    await message.reply("Укажите геопозицию места в виде маркера на карте и мы вычислим прогноз погоды.",
                        reply_markup=keyboard)


@dp.message_handler(state=Weather.location, content_types=['location'])
async def process_location(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.location

    location = data['location']
    latitude = location['latitude']
    longitude = location['longitude']
    position = str(latitude) + ',' + str(longitude)
    forecast = await weather.current(position)
    text = current_weather_format(forecast)
    user = message['from']
    logger.write('\n' + user.first_name + ' ' + user.last_name + '\n' + text[0] + '\n', 'debug')

    await message.reply(text=text[0], reply=False, reply_markup=ReplyKeyboardRemove())
    await message.reply(text=text[1], reply=False)
    await state.finish()
