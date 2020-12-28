from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor

from config import (BOT_TOKEN, SKIP_UPDATES, ADMIN_ID, weatherapi_url, weatherapi_key)
from weather.weatherapi import WeatherApiV1


storage = MemoryStorage()
weather = WeatherApiV1(weatherapi_url, weatherapi_key)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
executor = Executor(dp, skip_updates=SKIP_UPDATES)
