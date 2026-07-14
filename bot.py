import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database import init_db


# handlers

from handlers.start import router as start_router
from handlers.registration import router as registration_router
from handlers.admin import router as admin_router
from handlers.language import router as language_router


async def main():

    # создаем базу данных

    await init_db()


    # создаем бота

    bot = Bot(

        token=BOT_TOKEN

    )


    # диспетчер

    dp = Dispatcher()


    # подключаем обработчики

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


    # запуск

    await dp.start_polling(

        bot

    )



if __name__ == "__main__":

    asyncio.run(main())