import asyncio
import asyncpg
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv
from pathlib import Path
import random
import uuid

# Загрузка .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print(env_path)

POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

print('\n', DB_HOST, '\n',
        DB_PORT, '\n',
        DB_USER, '\n',
        DB_PASSWORD, '\n',
        POSTGRES_DB, '\n')

async def uuid_gen(sender_id, email):
    user_uuid = await str(sender_id) + str(uuid.uuid4()) + 'email:' +str(email)
    return user_uuid

async def creating_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD):
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=POSTGRES_DB, host=DB_HOST, port=DB_PORT
    )
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                sender_id BIGINT NOT NULL UNIQUE,
                user_uuid TEXT UNIQUE NOT NULL UNIQUE,
                email TEXT UNIQUE DEFAULT NULL,
                sub_type TEXT DEFAULT NULL,
                sub_link TEXT UNIQUE DEFAULT NULL,
                reg_date DATE DEFAULT NULL,
                sub_expiration DATE DEFAULT NULL,
                deleted_acc INTEGER DEFAULT 0 CHECK (deleted_acc IN (0, 1))
            );
        """)
    finally:
        await conn.close()


async def add_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, email):
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=POSTGRES_DB, host=DB_HOST, port=DB_PORT
    )
    try:
        user_uuid = await uuid_gen(sender_id, email)
        await conn.execute('''
            INSERT INTO users (sender_id, email, reg_date, user_uuid)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (sender_id) DO NOTHING
        ''', sender_id, email, datetime.now(), user_uuid)
    finally:
        await conn.close()


async def buy_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, num_month, sub_type, sub_link):
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=POSTGRES_DB, host=DB_HOST, port=DB_PORT
    )
    try:
        await conn.execute('''
            UPDATE users
            SET sub_type = $1, sub_expiration = $2 
            WHERE sender_id = $3
        ''', sub_type, datetime.now() + relativedelta(months=num_month), sender_id)
    finally:
        await conn.close()


async def url_sub_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, num_month, sub_type, sub_link):
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=POSTGRES_DB, host=DB_HOST, port=DB_PORT
    )
    try:
        await conn.execute('''
            UPDATE users
            SET sub_link = $1
            WHERE sender_id = $2
        ''', sub_link, sender_id)
    finally:
        await conn.close()


async def delete_toogle_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id):
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=POSTGRES_DB, host=DB_HOST, port=DB_PORT
    )
    try:
        await conn.execute('''
            UPDATE users
            SET deleted_acc = 1 - deleted_acc
            WHERE sender_id = $1
        ''', sender_id)
    finally:
        await conn.close()


async def show_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id):
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=POSTGRES_DB, host=DB_HOST, port=DB_PORT
    )
    try:
        row = await conn.fetchrow('''
            SELECT * FROM users 
            WHERE sender_id=$1
        ''', sender_id)
        if row:
            return dict(row)
        return None
    finally:
        await conn.close()

async def show_all_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD):
    conn = await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=POSTGRES_DB, host=DB_HOST, port=DB_PORT
    )
    try:
        rows = await conn.fetch('SELECT * FROM users')
        return [dict(row) for row in rows]  # возвращаем список словарей
    finally:
        await conn.close()



# Для тестирования
async def main():
    sender_id = random.randint(1000, 9999)
    email = f"user{sender_id}@example.com"

    await creating_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)
    await add_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, email)
    user = await show_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id)
    print(user, '\n')
    user_all = await show_all_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)
    for user in user_all:
        print(user)
    

if __name__ == "__main__":
    asyncio.run(main())
