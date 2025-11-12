import asyncpg
import asyncio
from dotenv import load_dotenv
from pathlib import Path
import os

# Загрузка .env
env_path = Path(__file__).resolve().parent / ".env"
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
