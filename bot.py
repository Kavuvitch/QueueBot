import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

import database


# handlers

from handlers.start import router as start_router
from handlers.registration import router as registration_router
from handlers.admin import router as admin_router
from handlers.language import router as language_router

print("TEST RAILWAY")

async def main():

    # подключаем PostgreSQL и создаём таблицу

    await database.init_db()


    # создаём бота

    bot = Bot(
        token=BOT_TOKEN
    )


    # создаём диспетчер

    dp = Dispatcher()


    # подключаем роутеры

    dp.include_router(
        start_router
    )

    dp.include_router(
        registration_router
    )

    dp.include_router(
        admin_router
    )

    dp.include_router(
        language_router
    )


    print("Bot started")


    try:

        await dp.start_polling(
            bot
        )


    finally:

        # закрываем соединение Telegram

        await bot.session.close()


        # закрываем PostgreSQL

        if database.pool:

            await database.pool.close()



if __name__ == "__main__":

    asyncio.run(main())