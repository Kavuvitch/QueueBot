from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import set_language

from keyboards import main_menu

from texts import TEXTS


router = Router()


# ==========================
# Арабский
# ==========================

@router.callback_query(
    F.data == "lang_ar"
)
async def set_arabic(
    callback: CallbackQuery
):

    user_id = callback.from_user.id


    await set_language(

        user_id,

        "ar"

    )


    await callback.message.answer(

        TEXTS["ar"]["welcome"],

        reply_markup=main_menu("ar")

    )


    await callback.answer()



# ==========================
# Английский
# ==========================

@router.callback_query(
    F.data == "lang_en"
)
async def set_english(
    callback: CallbackQuery
):

    user_id = callback.from_user.id


    await set_language(

        user_id,

        "en"

    )


    await callback.message.answer(

        TEXTS["en"]["welcome"],

        reply_markup=main_menu("en")

    )


    await callback.answer()