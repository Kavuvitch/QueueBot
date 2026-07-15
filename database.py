import asyncpg
import os
from datetime import datetime


DATABASE_URL = os.getenv("DATABASE_URL")

pool = None


# ==========================
# Создание базы
# ==========================

async def init_db():

    global pool

    pool = await asyncpg.create_pool(
        DATABASE_URL
    )

    async with pool.acquire() as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(

            telegram_id BIGINT PRIMARY KEY,

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


# ==========================
# Пользователь существует?
# ==========================

async def user_exists(user_id):

    async with pool.acquire() as db:

        user = await db.fetchrow(
            """
            SELECT telegram_id 
            FROM users 
            WHERE telegram_id=$1
            """,
            user_id
        )

        return user


# ==========================
# Создать пользователя
# ==========================

async def create_user(user):

    async with pool.acquire() as db:

        last_application = await db.fetchval(
            """
            SELECT MAX(application_number)
            FROM users
            """
        )


        if last_application is None:
            application = 12584
        else:
            application = last_application + 1


        await db.execute(
            """
            INSERT INTO users(

                telegram_id,
                first_name,
                last_name,
                username,
                language,
                application_number,
                created_at

            )

            VALUES(
                $1,$2,$3,$4,$5,$6,$7
            )
            """,

            user.id,
            user.first_name,
            user.last_name,
            user.username,
            "ar",
            application,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        )


# ==========================
# Получить пользователя
# ==========================

async def get_user(user_id):

    async with pool.acquire() as db:

        user = await db.fetchrow(
            """
            SELECT *
            FROM users
            WHERE telegram_id=$1
            """,
            user_id
        )


        print(
            "GET USER:",
            user
        )


        return user


# ==========================
# Получить язык
# ==========================

async def get_language(user_id):

    async with pool.acquire() as db:

        lang = await db.fetchval(
            """
            SELECT language
            FROM users
            WHERE telegram_id=$1
            """,
            user_id
        )


        if lang:
            return lang

        return "ar"


# ==========================
# Изменить язык
# ==========================

async def set_language(user_id, lang):

    async with pool.acquire() as db:

        await db.execute(
            """
            UPDATE users
            SET language=$1
            WHERE telegram_id=$2
            """,
            lang,
            user_id
        )


# ==========================
# Сохранить телефон
# ==========================

async def save_phone(user_id, phone):

    async with pool.acquire() as db:

        await db.execute(
            """
            UPDATE users
            SET phone=$1
            WHERE telegram_id=$2
            """,
            phone,
            user_id
        )


# ==========================
# Сохранить переднюю сторону
# ==========================

async def save_front(user_id, file_id):

    async with pool.acquire() as db:

        await db.execute(
            """
            UPDATE users
            SET front_photo=$1
            WHERE telegram_id=$2
            """,
            file_id,
            user_id
        )


# ==========================
# Сохранить заднюю сторону
# ==========================

async def save_back(user_id, file_id):

    async with pool.acquire() as db:

        await db.execute(
            """
            UPDATE users
            SET back_photo=$1
            WHERE telegram_id=$2
            """,
            file_id,
            user_id
        )

# ==========================
# Сохранить селфи
# ==========================

async def save_selfie(user_id, file_id):

    async with pool.acquire() as db:

        result = await db.execute(
            """
            UPDATE users
            SET selfie_photo=$1
            WHERE telegram_id=$2
            """,
            file_id,
            user_id
        )

        print(
            "SELFIE UPDATED:",
            result
        )


# ==========================
# Изменить статус
# ==========================

async def set_status(user_id, status):

    async with pool.acquire() as db:

        await db.execute(
            """
            UPDATE users
            SET status=$1
            WHERE telegram_id=$2
            """,
            status,
            user_id
        )


# ==========================
# Одобрить пользователя
# ==========================

async def approve_user(user_id):

    async with pool.acquire() as db:

        last_queue = await db.fetchval(
            """
            SELECT MAX(queue_number)
            FROM users
            """
        )


        if last_queue is None:
            queue_number = 301
        else:
            queue_number = last_queue + 1


        await db.execute(
            """
            UPDATE users
            SET
                status=$1,
                queue_number=$2
            WHERE telegram_id=$3
            """,
            "approved",
            queue_number,
            user_id
        )


    return queue_number



# ==========================
# Отклонить пользователя
# ==========================

async def reject_user(user_id):

    async with pool.acquire() as db:

        await db.execute(
            """
            UPDATE users

            SET

                status='rejected',

                front_photo=NULL,

                back_photo=NULL,

                selfie_photo=NULL

            WHERE telegram_id=$1

            """,
            user_id
        )


# ==========================
# Получить всех пользователей
# ==========================

async def get_all_users():

    async with pool.acquire() as db:

        users = await db.fetch(
            """
            SELECT *
            FROM users
            ORDER BY application_number
            """
        )

        return users



# ==========================
# Количество пользователей
# ==========================

async def get_users_count():

    async with pool.acquire() as db:

        count = await db.fetchval(
            """
            SELECT COUNT(*)
            FROM users
            """
        )

        return count



# ==========================
# Одобренные пользователи
# ==========================

async def get_approved_users():

    async with pool.acquire() as db:

        users = await db.fetch(
            """
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

            """
        )

        return users

async def init_db():

    global pool

    print("DATABASE_URL =", DATABASE_URL)

    pool = await asyncpg.create_pool(
        DATABASE_URL
    )