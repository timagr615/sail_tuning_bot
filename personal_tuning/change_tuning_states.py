from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import dp, bot
from aiogram.dispatcher import FSMContext
from db.crud import find_tuning_by_id, update_tuning_by_params
from db.utils import show_all_personal_tunings, show_personal_tuning, choice_filters_for_tuning, \
    find_personal_tunings_by_filter
from db.database import SessionLocal


class ChangeTuning(StatesGroup):
    tuning_id = State()
    param = State()
    param_value = State()


def get_inline_keyboard(tuning_id: str) -> InlineKeyboardMarkup:
    inline = InlineKeyboardMarkup()
    callback_data_1 = 'tid' + str(tuning_id) + ' mast_rake'
    callback_data_2 = 'tid' + str(tuning_id) + ' prebend'
    callback_data_3 = 'tid' + str(tuning_id) + ' tension'
    callback_data_4 = 'tid' + str(tuning_id) + ' mast_step'
    inline_btn_1 = InlineKeyboardButton('Завал', callback_data=callback_data_1)
    inline_btn_2 = InlineKeyboardButton('Пребенд', callback_data=callback_data_2)
    inline_btn_3 = InlineKeyboardButton('Натяжение на штаге', callback_data=callback_data_3)
    inline_btn_4 = InlineKeyboardButton('Дырка степса', callback_data=callback_data_4)
    inline.add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4)
    return inline


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change_id'))
async def process_callback_change(callback_query: CallbackQuery):
    tuning_id = callback_query.data[9:]

    kbd = get_inline_keyboard(tuning_id)
    await bot.send_message(
        callback_query.from_user.id,
        'Выберите параметр для изменения. Допускается редактирование всех параметров по очереди.',
        reply_markup=kbd,
    )
    # await ChangeTuning.param.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('tid'))
async def process_change_parameter(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(' ')
    tuning_id = data[0][3:]
    param = data[1]
    await ChangeTuning.param_value.set()
    async with state.proxy() as data:
        data['tuning_id'] = int(tuning_id)
        data['param'] = param

    await bot.send_message(
        callback_query.from_user.id,
        'Введите новое значение',
    )


@dp.message_handler(lambda message: message.text, state=ChangeTuning.param_value)
async def process_param_value(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['param_value'] = message.text

    # здесь должно быть изменение настроек
    db = SessionLocal()
    update_tuning_by_params(db, params=data)
    db.close()
    await state.finish()
    await message.answer(
        'Параметр сохранен. Продолжайте изменение или перейдите к любой другой команде.'
    )
