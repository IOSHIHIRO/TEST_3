from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_toc import database

dz_router = Router()

class Review(StatesGroup):
    name = State()
    word_gru = State()
    nom = State()
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
    await state.set_state(Review.word_gru)
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

@dz_router.message(Review.word_gru)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(word_gru=message.text)
    await state.set_state(Review.nom)
    await message.answer("Теперь введи номер дзшки (от 1 до 8)")

@dz_router.message(Review.nom)
async def process(message: types.Message, state: FSMContext):
    nom = message.text
    if not nom.isdigit():
        await message.answer("Вводите только цифры")
        return
    await state.update_data(nom=message.text)
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
               INSERT INTO homeworks (name, word_gru, nom, link)
               VALUES (?, ?, ?, ?)
               """,
        params=(data['name'], data['word_gru'], data['nom'], data['link']),
    )
    await state.clear()



@dz_router.callback_query(F.data == 'dz')
async def review_us(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Review.name)
    await callback.message.answer('Как вас зовут?')