import aiosqlite
from datetime import datetime

DATABASE = "users.db"

# ==========================
# Создание базы
# ==========================

async def init_db():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(

            telegram_id INTEGER PRIMARY KEY,

            first_name TEXT,
            last_name TEXT,
            username TEXT,

            phone TEXT,

            language TEXT DEFAULT 'ar',

            application_number INTEGER,

            queue_number INTEGER,

            status TEXT DEFAULT 'new',

            front_photo TEXT,
            back_photo TEXT,
            selfie_photo TEXT,

            created_at TEXT

        )
        """)

        await db.commit()


# ==========================
# Пользователь существует?
# ==========================

async def user_exists(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(

            "SELECT telegram_id FROM users WHERE telegram_id=?",

            (user_id,)

        )

        return await cursor.fetchone()


# ==========================
# Создать пользователя
# ==========================

async def create_user(user):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(

            "SELECT MAX(application_number) FROM users"

        )

        result = await cursor.fetchone()

        if result[0] is None:
            application = 12584
        else:
            application = result[0] + 1

        await db.execute("""

        INSERT INTO users(

            telegram_id,
            first_name,
            last_name,
            username,
            language,
            application_number,
            created_at

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            user.id,
            user.first_name,
            user.last_name,
            user.username,
            "ar",
            application,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        )

        )

        await db.commit()


# ==========================
# Получить пользователя
# ==========================

async def get_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            "SELECT * FROM users WHERE telegram_id=?",
            (user_id,)
        )

        user = await cursor.fetchone()

        print(
            "GET USER:",
            user
        )

        return user


# ==========================
# Получить язык
# ==========================

async def get_language(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(

            "SELECT language FROM users WHERE telegram_id=?",

            (user_id,)

        )

        result = await cursor.fetchone()

        if result:
            return result[0]

        return "ar"



# ==========================
# Изменить язык
# ==========================

async def set_language(user_id, lang):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(

            "UPDATE users SET language=? WHERE telegram_id=?",

            (

                lang,
                user_id

            )

        )

        await db.commit()


# ==========================
# Телефон
# ==========================

async def save_phone(user_id, phone):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(

            "UPDATE users SET phone=? WHERE telegram_id=?",

            (

                phone,
                user_id

            )

        )

        await db.commit()


# ==========================
# Передняя сторона
# ==========================

async def save_front(user_id, file_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(

            "UPDATE users SET front_photo=? WHERE telegram_id=?",

            (

                file_id,
                user_id

            )

        )

        await db.commit()


# ==========================
# Задняя сторона
# ==========================

async def save_back(user_id, file_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(

            "UPDATE users SET back_photo=? WHERE telegram_id=?",

            (

                file_id,
                user_id

            )

        )

        await db.commit()


# ==========================
# Селфи
# ==========================

async def save_selfie(user_id, file_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            UPDATE users 
            SET selfie_photo=? 
            WHERE telegram_id=?
            """,
            (
                file_id,
                user_id
            )
        )

        await db.commit()

        print(
            "SELFIE UPDATED:",
            cursor.rowcount
        )


# ==========================
# Изменить статус
# ==========================

async def set_status(user_id, status):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(

            "UPDATE users SET status=? WHERE telegram_id=?",

            (

                status,
                user_id

            )

        )

        await db.commit()


# ==========================
# Одобрить пользователя
# ==========================

async def approve_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        # ищем последний номер очереди
        cursor = await db.execute(
            """
            SELECT MAX(queue_number)
            FROM users
            """
        )

        result = await cursor.fetchone()

        if result[0] is None:
            queue_number = 301
        else:
            queue_number = result[0] + 1


        await db.execute(
            """
            UPDATE users
            SET status = ?,
                queue_number = ?
            WHERE telegram_id = ?
            """,
            (
                "approved",
                queue_number,
                user_id
            )
        )

        await db.commit()


    return queue_number


# ==========================
# Отклонить пользователя
# ==========================

async def reject_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""

        UPDATE users

        SET

        status='rejected',

        front_photo=NULL,

        back_photo=NULL,

        selfie_photo=NULL

        WHERE telegram_id=?

        """,

        (

            user_id,

        )

        )

        await db.commit()


# ==========================
# Получить всех пользователей
# ==========================

async def get_all_users():

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(

            "SELECT * FROM users ORDER BY application_number"

        )

        return await cursor.fetchall()


# ==========================
# Количество пользователей
# ==========================

async def get_users_count():

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(

            "SELECT COUNT(*) FROM users"

        )

        result = await cursor.fetchone()

        return result[0]

async def get_approved_users():

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
        SELECT
            first_name,
            last_name,
            phone,
            queue_number,
            application_number,
            status
        FROM users
        ORDER BY
            queue_number ASC,
            application_number ASC
        """)

        return await cursor.fetchall()