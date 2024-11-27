import asyncio
import logging

from bot_toc import bot, dp, database
from handlers.start import start_router
from handlers.dz import dz_router

async def on_startup(bot):
    database.create_tables()

async def main():
    dp.include_router(start_router)
    dp.include_router(dz_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())