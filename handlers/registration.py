from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.fsm.context import FSMContext

from states import Registration

from database import (
    save_phone,
    save_front,
    save_back,
    save_selfie,
    set_status,
    get_language,
    get_user
)

from keyboards import (
    main_menu,
    admin_keyboard
)

from texts import TEXTS
from config import ADMIN_IDS

import re

router = Router()


# ==================================================
# НАЧАЛО РЕГИСТРАЦИИ
# ==================================================

@router.callback_query(F.data == "agree")
async def start_registration(
        callback: CallbackQuery,
        state: FSMContext
):

    lang = await get_language(
        callback.from_user.id
    )

    keyboard = ReplyKeyboardMarkup(

        keyboard=[

            [
                KeyboardButton(
                    text="📱 مشاركة رقم الهاتف",
                    request_contact=True
                )
            ],

            [
                KeyboardButton(
                    text="✍️ إدخال رقم هاتف آخر"
                )
            ]

        ],

        resize_keyboard=True,
        one_time_keyboard=True

    )

    await callback.message.answer(

        "📱\n\nيرجى مشاركة رقم هاتفك أو اختيار إدخال رقم آخر.",

        reply_markup=keyboard

    )

    await state.set_state(
        Registration.phone
    )

    await callback.answer()


# ==================================================
# ПЕРЕХОД НА РУЧНОЙ ВВОД
# ==================================================

@router.message(
    Registration.phone,
    F.text.in_(
        [
            "✍️ إدخال رقم هاتف آخر",
            "✍️ Enter Another Phone Number"
        ]
    )
)
async def manual_phone(
        message: Message,
        state: FSMContext
):

    lang = await get_language(
        message.from_user.id
    )

    await state.set_state(
        Registration.manual_phone
    )

    if lang == "ar":

        await message.answer(

            "✍️\n\nيرجى كتابة رقم الهاتف مع رمز الدولة.\n\nمثال:\n+963912345678",

            reply_markup=ReplyKeyboardMarkup(

                keyboard=[],

                resize_keyboard=True

            )

        )

    else:

        await message.answer(

            "Please enter the phone number.\n\nExample:\n+9639XXXXXXXX"

        )


# ==================================================
# ПОЛУЧЕНИЕ КОНТАКТА TELEGRAM
# ==================================================

@router.message(
    Registration.phone,
    F.contact
)
async def get_phone(
        message: Message,
        state: FSMContext
):

    lang = await get_language(
        message.from_user.id
    )

    if message.contact.user_id != message.from_user.id:

        keyboard = ReplyKeyboardMarkup(

            keyboard=[

                [
                    KeyboardButton(
                        text="📱 مشاركة رقم الهاتف",
                        request_contact=True
                    )
                ],

                [
                    KeyboardButton(
                        text="✍️ إدخال رقم هاتف آخر"
                    )
                ]

            ],

            resize_keyboard=True,
            one_time_keyboard=True

        )

        await message.answer(

            "❌ يرجى مشاركة رقم هاتفك أو اختيار إدخال رقم آخر.",

            reply_markup=keyboard

        )

        return

    await save_phone(

        message.from_user.id,
        message.contact.phone_number

    )

    await message.answer(

        "✅ تم حفظ رقم الهاتف.",

        reply_markup=main_menu(lang)

    )

    await message.answer(

        TEXTS[lang]["front_photo"]

    )

    await state.set_state(
        Registration.front_id
    )


# ==================================================
# РУЧНОЙ ВВОД НОМЕРА
# ==================================================

@router.message(
    Registration.manual_phone
)
async def save_manual_phone(
        message: Message,
        state: FSMContext
):

    lang = await get_language(
        message.from_user.id
    )

    phone = message.text.replace(" ", "").strip()

    if not re.fullmatch(
            r"\+?\d{8,15}",
            phone
    ):
        if not phone.startswith("+"):
            phone = "+" + phone

        await message.answer(

            "❌ الرقم غير صحيح.\n\nمثال:\n+9639XXXXXXXX"

        )

        return

    await save_phone(

        message.from_user.id,
        phone

    )

    await message.answer(

        "✅ تم حفظ رقم الهاتف.",

        reply_markup=main_menu(lang)

    )

    await message.answer(

        TEXTS[lang]["front_photo"]

    )

    await state.set_state(
        Registration.front_id
    )

# ==================================================
# ФОТО ЛИЦЕВОЙ СТОРОНЫ ДОКУМЕНТА
# ==================================================

@router.message(Registration.front_id)
async def get_front_id(
        message: Message,
        state: FSMContext
):

    lang = await get_language(
        message.from_user.id
    )

    if not message.photo:

        await message.answer(
            TEXTS[lang]["front_photo"]
        )

        return

    file_id = message.photo[-1].file_id

    await save_front(
        message.from_user.id,
        file_id
    )

    await message.answer(
        TEXTS[lang]["back_photo"]
    )

    await state.set_state(
        Registration.back_id
    )


# ==================================================
# ФОТО ОБРАТНОЙ СТОРОНЫ ДОКУМЕНТА
# ==================================================

@router.message(Registration.back_id)
async def get_back_id(
        message: Message,
        state: FSMContext
):

    lang = await get_language(
        message.from_user.id
    )

    if not message.photo:

        await message.answer(
            TEXTS[lang]["back_photo"]
        )

        return

    file_id = message.photo[-1].file_id

    await save_back(
        message.from_user.id,
        file_id
    )

    await message.answer(
        TEXTS[lang]["selfie"]
    )

    await state.set_state(
        Registration.selfie_id
    )


# ==================================================
# СЕЛФИ С ДОКУМЕНТОМ
# ==================================================

@router.message(Registration.selfie_id)
async def get_selfie(
        message: Message,
        state: FSMContext,
        bot: Bot
):

    try:

        print("SELFIE START", message.from_user.id)


        lang = await get_language(
            message.from_user.id
        )


        if not message.photo:

            await message.answer(
                TEXTS[lang]["selfie"]
            )

            return


        file_id = message.photo[-1].file_id


        await save_selfie(
            message.from_user.id,
            file_id
        )

        print("SELFIE SAVED")


        await message.answer(
            "⏳ جاري إرسال الطلب...",
            reply_markup=main_menu(lang)
        )


        user = await get_user(
            message.from_user.id
        )


        print("USER DATA:", user)


        if not user:

            await message.answer(
                "❌ حدث خطأ. حاول مرة أخرى."
            )

            await state.clear()

            return


        phone = user[4]

        application_number = user[6]


        await set_status(
            message.from_user.id,
            "new"
        )


        caption = f"""
📥 Новая заявка

👤 {message.from_user.full_name}

🆔 {message.from_user.id}

📞 {phone}

📄 Заявка № {application_number}
"""


        print("START SENDING ADMINS")


        for admin_id in ADMIN_IDS:

            try:

                print(
                    "SEND TO ADMIN:",
                    admin_id
                )


                await bot.send_photo(
                    admin_id,
                    user[9],
                    caption=caption
                )


                await bot.send_photo(
                    admin_id,
                    user[10]
                )


                await bot.send_photo(
                    admin_id,
                    user[11],
                    reply_markup=admin_keyboard(
                        message.from_user.id
                    )
                )


                print(
                    "ADMIN SENT:",
                    admin_id
                )


            except Exception as e:

                print(
                    f"ADMIN ERROR {admin_id}: {repr(e)}"
                )


        await message.answer(
            TEXTS[lang]["waiting"],
            reply_markup=main_menu(lang)
        )


        await state.clear()


        print("SELFIE FINISHED")


    except Exception as e:

        print(
            "SELFIE GLOBAL ERROR:",
            repr(e)
        )


        await message.answer(
            "❌ حدث خطأ. حاول مرة أخرى."
        )

        await state.clear()