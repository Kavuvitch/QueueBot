from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from texts import TEXTS


# ==========================
# Главное меню
# ==========================

def main_menu(lang: str):

    if lang == "ar":

        return ReplyKeyboardMarkup(

            keyboard=[

                [
                    KeyboardButton(text="📝 التسجيل"),
                    KeyboardButton(text="🔢 ترتيبي")
                ],

                [
                    KeyboardButton(text="📢 آخر الإعلانات"),
                    KeyboardButton(text="❓ الأسئلة الشائعة")
                ],

                [
                    KeyboardButton(text="📞 التواصل معنا"),
                    KeyboardButton(text="💸 آلية استلام المساعدة")
                ],

                [
                    KeyboardButton(text="📋 شروط وأحكام التسجيل")
                ],

                [
                    KeyboardButton(text="🌍 اللغة")
                ]

            ],

            resize_keyboard=True

        )

    else:

        return ReplyKeyboardMarkup(

            keyboard=[

                [
                    KeyboardButton(text="📝 Registration"),
                    KeyboardButton(text="🔢 My Queue")
                ],

                [
                    KeyboardButton(text="📢 Latest News"),
                    KeyboardButton(text="❓ FAQ")
                ],

                [
                    KeyboardButton(text="📞 Contact Us"),
                    KeyboardButton(text="💸 How to Receive")
                ],

                [
                    KeyboardButton(text="📋 Rules")
                ],

                [
                    KeyboardButton(text="🌍 Language")
                ]

            ],

            resize_keyboard=True

        )


# ==========================
# Кнопка начала регистрации
# ==========================

def agree_keyboard(lang: str):

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text=TEXTS[lang]["agree_button"],

                    callback_data="agree"

                )

            ]

        ]

    )


# ==========================
# Выбор языка
# ==========================

def language_keyboard():

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text="🇸🇦 العربية",

                    callback_data="lang_ar"

                ),

                InlineKeyboardButton(

                    text="🇬🇧 English",

                    callback_data="lang_en"

                )

            ]

        ]

    )


# ==========================
# Админ-кнопки
# ==========================

def admin_keyboard(user_id: int):

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text="✅ قبول",

                    callback_data=f"approve_{user_id}"

                ),

                InlineKeyboardButton(

                    text="❌ رفض",

                    callback_data=f"reject_{user_id}"

                )

            ]

        ]

    )