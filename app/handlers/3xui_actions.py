from pathlib import Path
import os
from dotenv import load_dotenv
import DataBaseLib
from py3xui import AsyncApi

# Загрузка .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

XUI_HOST = os.getenv("XUI_HOST")
XUI_PORT = os.getenv("XUI_PORT")
XUI_USERNAME = os.getenv("XUI_USERNAME")
XUI_PASSWORD = os.getenv("XUI_PASSWORD")

XUI_HOST_FULL = str(f"http://{str(XUI_HOST)}:{str(XUI_PORT)}")

print(env_path)
print(XUI_HOST_FULL)


api = AsyncApi(XUI_HOST_FULL, XUI_USERNAME, XUI_PASSWORD)