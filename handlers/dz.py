from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_toc import database

dz_router = Router()

class Review(StatesGroup):
    name = State()
    group = State()
    number = State()
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
    await state.set_state(Review.group)
    msg = "Укажите группу: "
    kd = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='4701',
                    callback_data='4701'
                ),
                types.InlineKeyboardButton(
                    text='4702',
                    callback_data='4702'
                ),
                types.InlineKeyboardButton(
                    text='4703',
                    callback_data='4703'
                ),
                types.InlineKeyboardButton(
                    text='4704',
                    callback_data='4704'
                )
            ]
        ]
    )
    await message.answer(msg, reply_markup=kd)

@dz_router.callback_query(F.data.in_ (['4701','4702','4703','4704']),)
async def badly_us(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(group=callback.data)
    await state.set_state(Review.number)
    await callback.message.answer("Номер ДЗ")

@dz_router.message(Review.number)
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
              INSERT INTO homeworks (name, group_name, number_gr, link)
              VALUES (?,?,?,?)
              """,
            params=(data['name'], data['group_name'], data['number_gr'], data['link'])
        )
    await state.clear()

@dz_router.callback_query(F.data == 'dz')
async def review_us(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Review.name)
    await callback.message.answer('Как вас зовут?')