from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_toc import database

dz_router = Router()

class Review(StatesGroup):
    name = State()
    group_name = State()
    number_gr = State()
    link = State()

@dz_router.message(Command("dz"))
async def dz(message: types.Message, state: FSMContext):
    await state.set_state(Review.name)
    await message.answer('Как вас зовут? ')

@dz_router.message(Review.name)
async def process(message: types.Message, state: FSMContext):
    name = message.text
    if not name.istitle():
        await message.answer('Имя должно начинаться с заглавной буквы.')
        return
    await state.update_data(name=message.text)
    await state.set_state(Review.group_name)
    group_kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Группа 43-1"),
                types.KeyboardButton(text="Группа 44-1"),
            ],
            [
                types.KeyboardButton(text="Группа 45-1"),
                types.KeyboardButton(text="Группа 46-1"),
            ],
            [
                types.KeyboardButton(text="Группа 47-1"),
                types.KeyboardButton(text="Группа 48-1"),
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer("Теперь введи название своей группы", reply_markup=group_kb)

@dz_router.message(Review.group_name)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group_dz=message.text)
    await state.set_state(Review.number_gr)
    await message.answer("Теперь введи номер дзшки (от 1 до 8)")

@dz_router.message(Review.number_gr)
async def process(message: types.Message, state: FSMContext):
    number = message.text
    if not number.isdigit():
        await message.answer("Вводите только цифры")
        return
    await state.update_data(number=message.text)
    await state.set_state(Review.link)
    await message.answer("Ссылка на гитхаб")

@dz_router.message(Review.link)
async def process(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer('ДЗ отправлено')

    data = await state.get_data()
    print(data)

    database.execute(
        query=""" 
               INSERT INTO homeworks (name, group_dz, number_dz, link)
               VALUES (?, ?, ?, ?)
               """,
        params=(data["name"], data["name_group"], data["number_gr"], data["link"]),
    )

    await state.clear()

@dz_router.callback_query(F.data == 'dz')
async def review_us(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Review.name)
    await callback.message.answer('Как вас зовут?')