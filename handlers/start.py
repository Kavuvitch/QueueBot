from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from database import (
    user_exists,
    create_user,
    get_language,
    get_user
)

from keyboards import (
    main_menu,
    agree_keyboard,
    language_keyboard
)

from texts import TEXTS

from config import SUPPORT_CONTACT

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def phone_keyboard(lang: str):

    if lang == "ar":

        return ReplyKeyboardMarkup(

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

    return ReplyKeyboardMarkup(

        keyboard=[

            [
                KeyboardButton(
                    text="📱 Share Phone Number",
                    request_contact=True
                )
            ],

            [
                KeyboardButton(
                    text="✍️ Enter Another Phone Number"
                )
            ]

        ],

        resize_keyboard=True,
        one_time_keyboard=True

    )

router = Router()


# ==========================
# /start
# ==========================

@router.message(CommandStart())
async def start(message: Message):

    user = message.from_user

    if not await user_exists(user.id):
        await create_user(user)

    lang = await get_language(user.id)

    await message.answer(

        TEXTS[lang]["welcome"],

        reply_markup=main_menu(lang)

    )


# ==========================
# Регистрация
# ==========================

@router.message(lambda m: m.text in ["📝 التسجيل", "📝 Registration"])
async def registration(message: Message):

    lang = await get_language(message.from_user.id)

    user = await get_user(message.from_user.id)

    # Если пользователь уже зарегистрирован
    if user and user[4]:

        if lang == "ar":

            await message.answer(
                """
✅ لقد قمت بالتسجيل بالفعل.

لا يمكن إرسال أكثر من طلب باستخدام نفس الحساب.
"""
            )

        else:

            await message.answer(
                """
✅ You have already registered.

Only one application is allowed per account.
"""
            )

        return

    await message.answer(

        TEXTS[lang]["register_info"],

        reply_markup=agree_keyboard(lang)

    )


# ==========================
# FAQ
# ==========================

@router.message(lambda m: m.text in ["❓ الأسئلة الشائعة", "❓ FAQ"])
async def faq(message: Message):

    lang = await get_language(message.from_user.id)

    await message.answer(

        TEXTS[lang]["faq"]

    )


# ==========================
# Новости
# ==========================

@router.message(lambda m: m.text in ["📢 آخر الإعلانات", "📢 Latest News"])
async def news(message: Message):

    lang = await get_language(message.from_user.id)

    if lang == "ar":

        news_text = "لا توجد إعلانات جديدة حاليًا."

    else:

        news_text = "There are no new announcements at the moment."

    await message.answer(

        TEXTS[lang]["news"].format(news_text)

    )


# ==========================
# Поддержка
# ==========================

@router.message(lambda m: m.text in ["📞 التواصل معنا", "📞 Contact Us"])
async def support(message: Message):

    lang = await get_language(message.from_user.id)

    await message.answer(

        TEXTS[lang]["support"].format(SUPPORT_CONTACT)

    )
# ==========================
# Как получить помощь
# ==========================

@router.message(
    lambda m: m.text in [
        "💸 آلية استلام المساعدة",
        "💸 How to Receive"
    ]
)
async def receive_help(message: Message):

    lang = await get_language(
        message.from_user.id
    )

    await message.answer(
        TEXTS[lang]["receive_help"]
    )

# ==========================
# Правила
# ==========================

@router.message(lambda m: m.text in ["📋 شروط وأحكام التسجيل", "📋 Rules"])
async def rules(message: Message):

    lang = await get_language(message.from_user.id)

    await message.answer(

        TEXTS[lang]["rules"]

    )


# ==========================
# Очередь
# ==========================

# ==========================
# Очередь
# ==========================

@router.message(lambda m: m.text in ["🔢 ترتيبي", "🔢 My Queue"])
async def queue(message: Message):

    lang = await get_language(message.from_user.id)

    user = await get_user(message.from_user.id)

    if not user:

        await message.answer(
            "❌ لم يتم العثور على طلبك."
        )

        return


    application = user[6]
    queue_number = user[7]
    status = user[8]


    if status != "approved":

        await message.answer(

            TEXTS[lang]["queue_wait"]

        )

        return


    await message.answer(

        TEXTS[lang]["approved"].format(

            application,

            queue_number

        )

    )


# ==========================
# Язык
# ==========================

@router.message(lambda m: m.text in ["🌍 اللغة", "🌍 Language"])
async def language(message: Message):

    await message.answer(

        "🌍",

        reply_markup=language_keyboard()

    )