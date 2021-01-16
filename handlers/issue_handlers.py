from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from bot import dp
from db import crud
from aiogram.dispatcher import FSMContext
from db.database import SessionLocal


class CreateIssue(StatesGroup):
    issue = State()


@dp.message_handler(commands='issue')
async def issue(message: Message):
    await CreateIssue.issue.set()
    await message.answer('Введите подробное описание вопроса или ошибки и мы обязательно его рассмотрим в '
                         'ближайшее время')


@dp.message_handler(lambda message: message.text, state=CreateIssue.issue)
async def process_issue(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['issue'] = message.text
    db = SessionLocal()
    crud.create_issue(db, data['issue'], message)
    db.close()
    await message.answer('Благодарим за предоставленную информацию, мы рассмотрим её в ближайшее время!')
    await state.finish()
