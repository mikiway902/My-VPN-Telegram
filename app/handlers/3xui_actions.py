import asyncio
from pathlib import Path
import os
from dotenv import load_dotenv
from py3xui import AsyncApi, Inbound, Settings, StreamSettings, Sniffing
import py3xui

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

XUI_HOST_FULL = f"http://{XUI_HOST}:{XUI_PORT}".rstrip("/")

print(f"ENV path: {env_path}")
print(f"XUI full host: {XUI_HOST_FULL}")


async def login_3xui(XUI_HOST_FULL, XUI_USERNAME, XUI_PASSWORD):
    api = AsyncApi(XUI_HOST_FULL, XUI_USERNAME, XUI_PASSWORD)
    await api.login()

    # Проверяем успешный логин
    if not await api.check_login():
        print("❌ Не удалось войти в XUI панель")
        return

    print("✅ Успешный логин в XUI")

    # Настройки inbound
    settings = Settings(
        clients=[{
            "id": "uuid-вставь-свой",
            "flow": "",
            "email": "test@example.com"
        }]
    )

    sniffing = Sniffing(enabled=True, dest_override=["http", "tls"])

    tcp_settings = {
        "acceptProxyProtocol": False,
        "header": {"type": "none"},
    }

    stream_settings = StreamSettings(
        network="tcp",
        security="none",
        tcp_settings=tcp_settings,
    )

    inbound = Inbound(
        enable=True,
        port=443,
        protocol="vless",
        settings=settings,
        stream_settings=stream_settings,
        sniffing=sniffing,
        remark="test3"
    )

    # Добавляем inbound
    result = await api.inbound.add(inbound)
    print("✅ Inbound добавлен:", result)


if __name__ == "__main__":
    asyncio.run(login_3xui(XUI_HOST_FULL, XUI_USERNAME, XUI_PASSWORD))
