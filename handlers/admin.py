from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database import (
    approve_user,
    reject_user,
    get_user
)
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from texts import TEXTS

from config import ADMIN_IDS
from database import get_approved_users


router = Router()


# ==========================
# Проверка администратора
# ==========================

def is_admin(user_id):
    return int(user_id) in ADMIN_IDS



# ==========================
# Одобрение заявки
# ==========================

@router.callback_query(
    F.data.startswith("approve_")
)
async def approve_application(
    callback: CallbackQuery,
    bot: Bot
):
    if not is_admin(callback.from_user.id):

        await callback.answer(
            "Нет доступа",
            show_alert=True
        )

        return


    user_id = int(

        callback.data.split("_")[1]

    )


    # выдаем номер очереди

    queue_number = await approve_user(

        user_id

    )


    user = await get_user(

        user_id

    )


    application_number = user[6]


    lang = user[5]


    # Сообщение пользователю

    await bot.send_message(

        chat_id=user_id,

        text=TEXTS[lang]["approved"].format(

            application_number,

            queue_number

        )

    )


    await callback.message.edit_text(

        callback.message.text
        +
        "\n\n✅ Одобрено"

    )


    await callback.answer(

        "Пользователь одобрен"

    )



# ==========================
# Отклонение заявки
# ==========================

@router.callback_query(
    F.data.startswith("reject_")
)
async def reject_application(
    callback: CallbackQuery,
    bot: Bot
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "Нет доступа",
            show_alert=True
        )

        return


    user_id = int(

        callback.data.split("_")[1]

    )


    await reject_user(

        user_id

    )


    user = await get_user(

        user_id

    )


    lang = user[5]


    await bot.send_message(

        chat_id=user_id,

        text=TEXTS[lang]["rejected"]

    )


    await callback.message.edit_text(

        callback.message.text
        +
        "\n\n❌ Отклонено"

    )


    await callback.answer(

        "Заявка отклонена"

    )

@router.message(Command("backup"))
async def backup_database(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Access denied.")
        return

    await message.answer_document(
        FSInputFile("users.db"),
        caption="📦 Database backup"
    )

@router.message(Command("users"))
async def users_list(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        return

    users = await get_approved_users()

    if not users:
        await message.answer("База данных пуста.")
        return

    text = "📋 Список пользователей\n\n"

    for user in users:

        first_name = user[0] or ""
        last_name = user[1] or ""
        phone = user[2] or "Нет номера"
        queue = user[3] or "-"
        application = user[4]
        status = user[5]

        text += (
            f"👤 {first_name} {last_name}\n"
            f"📞 {phone}\n"
            f"📄 Заявка: {application}\n"
            f"🔢 Очередь: {queue}\n"
            f"📌 Статус: {status}\n\n"
        )

    # Telegram ограничивает сообщение 4096 символами
    for i in range(0, len(text), 4000):
        await message.answer(text[i:i+4000])