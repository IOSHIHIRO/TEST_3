from aiogram import Router,types,F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

start_router = Router()
user_id = set()


@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    nam_id = message.from_user.id
    user_id.add(nam_id)
    count_id = len(user_id)
    name = message.from_user.first_name
    msg = f"Выберите команды /dz"

    kob = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='/start')],
        ]
    )
    await message.answer(f'Привет, {name} наш бот обслуживает уже {count_id} пользователя.'
                         , reply_markup=kob)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Отправить домашнее задание",
                    callback_data="dz"
                )
            ]
        ]
    )

    await message.answer(msg, reply_markup=kb)


@start_router.callback_query(F.data == '/start')
async def start_us(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
