from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from bot import dp, weather
from aiogram.dispatcher import FSMContext
from db.crud import create_tuning
from db.database import SessionLocal
from config import logger


class PersonalTuning(StatesGroup):
    boat = State()
    sail_firm = State()
    sail_model = State()
    place = State()
    wind = State()
    gusts = State()
    wave_height = State()
    wave_length = State()
    crew_weight = State()
    mast_rake = State()
    prebend = State()
    tension = State()
    mast_step = State()
    chocks = State()
    spreraders_leng = State()
    quality = State()
    description = State()


@dp.message_handler(commands='create')
async def personal_start(message: Message):
    await PersonalTuning.boat.set()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("BlueBlue", "Mackay", "Ziegelmayer")
    await message.reply("Выберите фирму лодки", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["BlueBlue", "Mackay", "Ziegelmayer"],
                    state=PersonalTuning.boat)
async def boat_invalid(message: Message):
    return await message.reply("Нет такой фирмы лодки, выберите фирму с кнопки.")


@dp.message_handler(lambda message: message.text, state=PersonalTuning.boat)
async def process_sail_firm(message: Message, state: FSMContext):
    """
    Обработка геопозиции пользователя
    """
    async with state.proxy() as data:
        data['boat'] = message.text

    await PersonalTuning.next()
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("North", "Zaoli")
    await message.reply("Выберите фирму паруса", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Zaoli", "North"], state=PersonalTuning.sail_firm)
async def process_sail_invalid(message: Message):
    return await message.reply("Нет такой фирмы парусов в базе, выберите фирму с кнопки.")


@dp.message_handler(lambda message: message.text, state=PersonalTuning.sail_firm)
async def process_sail_model(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sail_firm'] = message.text

    await PersonalTuning.next()
    ReplyKeyboardRemove()
    if message.text == "Zaoli":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("R12.", "R14.", "R15.", "R16.")
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("N9-L5.", "N9-L5(H).", "N10-L5(H).", "N10-L5.", "N12-L9(B).", "N13-L16.", "N13-L12.", "N14-L18.")
    await message.reply('Какая у Вас модель паруса?', reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["R12.", "R14.", "R15.", "R16.", "N9-L5.", "N9-L5(H).",
                                                         "N10-L5(H).", "N10-L5.", "N12-L9(B).", "N13-L16.", "N13-L12.",
                                                         "N14-L18."], state=PersonalTuning.sail_model)
async def sail_model_invalid(message: Message):
    await message.reply('Выберите модель с кнопки.')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.sail_model)
async def process_place(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sail_model'] = message.text
    await PersonalTuning.next()
    ReplyKeyboardRemove()
    await message.reply('Укажите место в виде: Страна, Город')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.place)
async def process_place(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['place'] = message.text
    await PersonalTuning.next()
    await message.reply('Напишите силу ветра в узлах.')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.wind)
async def process_wind(message: Message, state: FSMContext):
    wind = float(message.text.replace(',', '.'))
    async with state.proxy() as data:
        data['wind'] = wind
    await PersonalTuning.next()
    await message.reply('Укажите силу порывов в узлах.')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.gusts)
async def process_gusts(message: Message, state: FSMContext):
    gusts = float(message.text.replace(',', '.'))
    async with state.proxy() as data:
        data['gusts'] = gusts
    await PersonalTuning.next()
    await message.reply('Укажите высоту волн в метрах.')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.wave_height)
async def process_waves(message: Message, state: FSMContext):
    waves = float(message.text.replace(',', '.'))
    async with state.proxy() as data:
        data['wave_height'] = waves
    await PersonalTuning.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Короткая', 'Средняя', 'Длинная')
    await message.reply('Укажите длину волн.', reply_markup=markup)


@dp.message_handler(lambda message: message.text, state=PersonalTuning.wave_length)
async def process_wave_len(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['wave_length'] = message.text
    await PersonalTuning.next()
    ReplyKeyboardRemove()
    await message.reply('Укажите вес экипажа в килограммах.')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.crew_weight)
async def process_crew(message: Message, state: FSMContext):
    crew = float(message.text.replace(',', '.'))
    async with state.proxy() as data:
        data['crew_weight'] = crew
    await PersonalTuning.next()
    await message.reply('Укажите завал в метрах (Например, 6.75).')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.mast_rake)
async def process_rake(message: Message, state: FSMContext):
    mast_rake = float(message.text.replace(',', '.'))
    async with state.proxy() as data:
        data['mast_rake'] = mast_rake
    await PersonalTuning.next()
    await message.reply('Укажите пребенд в миллиметрах (Например, 75).')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.prebend)
async def process_prebend(message: Message, state: FSMContext):
    prebend = float(message.text.replace(',', '.'))
    async with state.proxy() as data:
        data['prebend'] = prebend
    await PersonalTuning.next()
    await message.reply('Укажите натяжение на штаге (Например, 27.5).')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.tension)
async def process_tension(message: Message, state: FSMContext):
    tension = float(message.text.replace(',', '.'))
    async with state.proxy() as data:
        data['tension'] = tension
    await PersonalTuning.next()
    await message.reply('Укажите дырку переднего болта степса (Самая первая дырка: 0, потом 1 и т.д.).')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.mast_step)
async def process_step(message: Message, state: FSMContext):
    step = int(message.text)
    async with state.proxy() as data:
        data['mast_step'] = step
    await PersonalTuning.next()
    await message.reply('Укажите упор (Например: -1, 0.5)')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.chocks)
async def process_chocks(message: Message, state: FSMContext):
    chocks = message.text
    async with state.proxy() as data:
        data['chocks'] = chocks
    await PersonalTuning.next()
    await message.reply('Укажите длину краспиц в миллиметрах.')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.spreraders_leng)
async def process_spreraders(message: Message, state: FSMContext):
    spreraders = int(message.text)
    async with state.proxy() as data:
        data['spreraders_leng'] = spreraders
    await PersonalTuning.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('1', '2', '3', '4', '5')
    await message.reply('Укажите качетсво завала: 1 - очень плохой, 5 - отличный.', reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ['1', '2', '3', '4', '5'], state=PersonalTuning.quality)
async def process_quality_invalid(message: Message):
    return await message.reply("Выберите качество с кнопки с кнопки.")


@dp.message_handler(lambda message: message.text, state=PersonalTuning.quality)
async def process_quality(message: Message, state: FSMContext):
    quality = message.text
    async with state.proxy() as data:
        data['quality'] = quality
    ReplyKeyboardRemove()
    await PersonalTuning.next()
    await message.reply('Напишите короткое описание завала.')


@dp.message_handler(lambda message: message.text, state=PersonalTuning.description)
async def process_description(message: Message, state: FSMContext):
    description = message.text
    async with state.proxy() as data:
        data['description'] = description
    await message.answer(
        fmt.text(
            fmt.text(fmt.hunderline("Фирма лодки:"), data['boat']),
            fmt.text(fmt.hunderline("Фирма паруса:"), data['sail_firm']),
            fmt.text(fmt.hunderline("Модель паруса:"), data['sail_model']),
            fmt.text(fmt.hunderline("Место:"), data['place']),
            fmt.text(fmt.hunderline("Ветер:"), data['wind'], 'kt'),
            fmt.text(fmt.hunderline("Порывы:"), data['gusts'], 'kt'),
            fmt.text(fmt.hunderline("Высота волн:"), data['wave_height'], 'm'),
            fmt.text(fmt.hunderline("Длина волн:"), data['wave_length']),
            fmt.text(fmt.hunderline("Вес экипажа:"), data['crew_weight'], 'kg'),
            fmt.text(fmt.hunderline("Завал:"), data['mast_rake'], 'm'),
            fmt.text(fmt.hunderline("Пребенд:"), data['prebend'], 'mm'),
            fmt.text(fmt.hunderline("Натяжение на штаге:"), data['tension']),
            fmt.text(fmt.hunderline("Дырка степса:"), data['mast_step']),
            fmt.text(fmt.hunderline("Упор:"), data['chocks']),
            fmt.text(fmt.hunderline("Длина краспиц:"), data['spreraders_leng'], 'mm'),
            fmt.text(fmt.hunderline("Качество завала:"), data['quality']),
            fmt.text(fmt.hunderline("Описание:"), data['description']),
            sep="\n"
        ),
        parse_mode="HTML"
    )
    db = SessionLocal()
    create_tuning(db, message, data)
    db.close()
    await state.finish()
