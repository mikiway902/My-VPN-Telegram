import asyncpg
import asyncio
from dotenv import load_dotenv
from pathlib import Path
import os

# Загрузка .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = 'sladk'
DB_PASSWORD = 'synke345'

async def test_conn():
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=POSTGRES_DB
    )
    print("Connected!")
    await conn.close()

asyncio.run(test_conn())
