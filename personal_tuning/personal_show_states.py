from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import dp, weather, bot
from aiogram.dispatcher import FSMContext
from db.crud import show_all_personal_tunings, find_tuning_by_id, delete_tuning_by_id
from db.database import SessionLocal


class ShowTuning(StatesGroup):
    filter = State()
    custom_tuning = State()


def return_tuning_text(tuning):
    text = fmt.text(
        fmt.text('Лодка: ', tuning.boat),
        fmt.text('Фирма паруса: ', tuning.sail_firm),
        fmt.text('Модель паруса: ', tuning.sail_model),
        fmt.text('Место: ', tuning.place),
        fmt.text('Ветер: ', tuning.wind, 'kt'),
        fmt.text('Порывы: ', tuning.gusts, 'kt'),
        fmt.text('Высота волн:', tuning.wave_height, 'm'),
        fmt.text('Длина волн: ', tuning.wave_length),
        fmt.text('Вес экипажа: ', tuning.crew_weight, 'kg'),
        fmt.text('Завал: ', tuning.mast_rake, 'm'),
        fmt.text('Пребенд: ', tuning.prebend, 'mm'),
        fmt.text('Натяжение на штаге: ', tuning.tension),
        fmt.text('Дырка в степсе: ', tuning.mast_step),
        fmt.text('Упор: ', tuning.chocks),
        fmt.text('Длина краспиц: ', tuning.spreraders_leng, 'mm'),
        fmt.text('Качество: ', tuning.quality),
        fmt.text('Комментарии: ', tuning.description),
        sep='\n',
    )
    return text


def all_tunings_inline_kb(data):
    inline_kb = InlineKeyboardMarkup(row_width=3)
    for i, item in enumerate(data):
        text = item[3] + '\n' + item[2] + ', ' + str(item[4]) + ' kt'
        callback_data = 'id' + str(item[-1])
        inline_btn = InlineKeyboardButton(text, callback_data=callback_data)
        inline_kb.add(inline_btn)
    return inline_kb


@dp.message_handler(commands=['show'])
async def send_menu(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True,  one_time_keyboard=True)
    markup.add("Показать все мои настройки")
    markup.add("Отобразить доступные фильтры настроек")
    await message.reply("Как вы хотите подобрать настройку?", reply_markup=markup)


@dp.message_handler(regexp='Показать все мои настройки')
async def process_all_tunings(message: Message):
    user_id = message['from'].id
    db = SessionLocal()
    data = show_all_personal_tunings(db, user_id)
    db.close()
    inline_kb = all_tunings_inline_kb(data)
    if data:
        await message.reply(text='Ваши настройки: ', reply_markup=inline_kb)
    else:
        await message.reply(text='У вас пока нет записанных настроек!')


# Отображение выбранной с кнопки настройки
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('id'))
async def process_callback_tuning(callback_query: CallbackQuery):
    tuning_id = callback_query.data[2:]
    if tuning_id.isdigit():
        tuning_id = int(tuning_id)
    db = SessionLocal()
    tuning = find_tuning_by_id(db, tuning_id)
    db.close()
    # await bot.answer_callback_query(callback_query.id, text=tuning_id, show_alert=True)
    # await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! id={tuning_id}')
    inline_kb = InlineKeyboardMarkup()
    callback_data = 'del_id' + str(tuning_id)
    inline_btn = InlineKeyboardButton('Удалить настройку', callback_data=callback_data)
    inline_kb.add(inline_btn)
    await bot.send_message(
        callback_query.from_user.id,
        return_tuning_text(tuning),
        reply_markup=inline_kb,
        parse_mode="HTML",
    )


# Обработчик нажатия кпонки удаления настройки
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del_id'))
async def process_callback_delete(callback_query: CallbackQuery):
    tuning_id = callback_query.data[6:]
    if tuning_id.isdigit():
        tuning_id = int(tuning_id)
    db = SessionLocal()
    delete_tuning_by_id(db, tuning_id)
    db.close()

    await bot.send_message(
        callback_query.from_user.id,
        'Настройка удалена',
        parse_mode='HTML',
    )
