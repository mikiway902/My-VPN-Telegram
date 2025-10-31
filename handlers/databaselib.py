import asyncio
import asyncpg
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent() / ".env"

load_dotenv(dotenv_path=env_path)
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

async def get_connection():
    try:
        print(f"[+] Подключаемся к БД {POSTGRES_DB} на {DB_HOST}:{DB_PORT} как {DB_USER}")