from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as fmt
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from bot import dp, weather
from aiogram.dispatcher import FSMContext
from config import logger
from weather.weather_app import current_weather_format
from .methods import choice_tuning


class Tuning(StatesGroup):
    location = State()
    sail = State()
    model = State()


@dp.message_handler(commands='tuning')
async def tuning_start(message: Message):
    # Set state
    await Tuning.location.set()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Запросить геолокацию", request_location=True))
    await message.reply("Укажите геопозицию места гонок в виде маркера на карте.", reply_markup=keyboard)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Прервать выбор настроек
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.write(f'Закрытие состояния {current_state}', 'info')
    await state.finish()
    await message.reply('Прекращено.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Tuning.location, content_types=['location'])
async def process_location(message: Message, state: FSMContext):
    """
    Обработка геопозиции пользователя
    """
    async with state.proxy() as data:
        data['location'] = message.location

    await Tuning.next()
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Zaoli", "North")
    await message.reply("Выберите фирму паруса", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Zaoli", "North"], state=Tuning.sail)
async def process_sail_invalid(message: Message):
    """
    In this example sail has to be one of: Zaoli, North.
    """
    return await message.reply("Нет такой фирмы парусов в базе, выберите фирму с кнопки.")


@dp.message_handler(lambda message: message.text, state=Tuning.sail)
async def process_sail_model(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['sail'] = message.text

    await Tuning.next()
    ReplyKeyboardRemove()
    if message.text == 'Zaoli':
        markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("R12", "R14", "R15", "R16")
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("N9-L5", "N9-L5(H)", "N10-L5(H)", "N10-L5", "N12-L9(B)", "N13-L16", "N13-L12", "N14-L18")

    await message.reply("Какая у вас модель паруса?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["R12", "R14", "R15", "R16", "N9-L5", "N9-L5(H)", "N10-L5(H)",
                                                         "N10-L5", "N12-L9(B)", "N13-L16", "N13-L12", "N14-L18"],
                    state=Tuning.model)
async def process_sail_model_invalid(message: Message):
    return await message.reply("Нет такой модели парусов в базе, выберите модель с кнопки.")


@dp.message_handler(state=Tuning.model)
async def process_tuning(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['model'] = message.text

        markup = ReplyKeyboardRemove()

        await message.answer(
            fmt.text(
                fmt.text(fmt.hunderline("Sail: "), data['sail']),
                fmt.text(fmt.hunderline("Sail model:"), data['model']),
                sep="\n"
            ),
            reply_markup=markup,
            parse_mode="HTML"
        )

    location = data['location']
    latitude = location['latitude']
    longitude = location['longitude']
    position = str(latitude) + ',' + str(longitude)
    forecast = await weather.current(position)
    text = current_weather_format(forecast)
    await message.reply(text=text[0], reply=False)
    await message.reply(text=text[1], reply=False)
    cur = forecast['current']
    wind_kt = cur['wind_kph'] * 0.54
    gusts_kt = cur['gust_kph'] * 0.54
    avg_wind = round((wind_kt + gusts_kt)/2, 1)
    tuning = choice_tuning(data['sail'], data['model'], avg_wind)
    user = message['from']
    logger.write('\n' + 'TUNING' + '\n' + user.first_name + ' ' + user.last_name + '\n' + text[0] + '\n', 'debug')
    # print(message, data['sail'], location, text[0])
    await message.answer(
        fmt.text(
            fmt.text(fmt.hunderline("Фирма:"), tuning['Фирма']),
            fmt.text(fmt.hunderline("Модель паруса:"), tuning["Модель паруса"]),
            fmt.text(fmt.hunderline("Ветер:"), tuning["Ветер"]),
            fmt.text(fmt.hunderline("Ветер завала:"), tuning["Ветер завала"]),
            fmt.text(fmt.hunderline("Завал:"), tuning["Завал"]),
            fmt.text(fmt.hunderline("Пребенд:"), tuning["Пребенд"]),
            fmt.text(fmt.hunderline("Натяжение на штаге:"), tuning["Натяжение на штаге"]),
            fmt.text(fmt.hunderline("Дырка в степсе:"), tuning["Дырка в степсе"]),
            fmt.text(fmt.hunderline("Упор:"), tuning["Упор"]),
            fmt.text(fmt.hunderline("Длина краспиц:"), tuning["Длина краспиц"]),
            sep="\n"
        ),
        reply_markup=markup,
        parse_mode="HTML"
    )
    # Finish conversation
    await state.finish()
