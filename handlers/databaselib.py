import asyncio
import asyncpg
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv
from pathlib import Path
import random

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


async def creating_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD):
    async with asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=POSTGRES_DB,
        host=DB_HOST,
        port=DB_PORT) as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users(
                sender_id TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE DEFAULT NULL,
                sub_type TEXT DEFAULT NULL,
                sub_link TEXT UNIQUE DEFAULT NULL,
                reg_date DATE DEFAULT NULL,
                sub_expiration DATE DEFAULT NULL
                )
                           ''')
        
async def add_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, email):
    async with asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=POSTGRES_DB,
        host=DB_HOST,
        port=DB_PORT) as conn:
        await conn.execute('''
            INSERT INTO users (sender_id, email, reg_date) 
            VALUES($1, $2, $3)
            ON CONFLICT (sender_id) DO NOTHING
                           ''', sender_id, email, datetime.now())
        
async def update_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, num_month, sub_type, sub_link):
    async with asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=POSTGRES_DB,
        host=DB_HOST,
        port=DB_PORT) as conn:
        await conn.execute('''
            UPDATE users
            SET sub_type = $1, sub_link = $2, sub_expiration = $3 
            WHERE sender_id = $4     
                           ''', sub_type, sub_link, datetime.now() + relativedelta(month=num_month), sender_id)

        
async def main():
    env_path = Path(__file__).resolve().parent() / ".env"

    load_dotenv(dotenv_path=env_path)
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    sender_id = random.range(0, 100, 5)
    email = random.range(0, 100, 5)
        
    creating_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)
    add_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, email)
    
    
if __name__ == "__main__":
    asyncio.run(main())