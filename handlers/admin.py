from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database import (
    approve_user,
    reject_user,
    get_user
)

from texts import TEXTS

from config import ADMIN_IDS


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