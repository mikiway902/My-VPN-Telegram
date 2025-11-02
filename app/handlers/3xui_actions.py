from pathlib import Path
import os
from dotenv import load_dotenv
import DataBaseLib
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

XUI_HOST_FULL = str(f"http://{str(XUI_HOST)}:{str(XUI_PORT)}")

print(env_path)
print(XUI_HOST_FULL)

async def login_3xui(XUI_HOST_FULL, XUI_USERNAME, XUI_PASSWORD):
    api = py3xui.AsyncApi(XUI_HOST_FULL, XUI_USERNAME, XUI_PASSWORD)
    await api.login()
    settings = Settings()
    sniffing = Sniffing(enabled=True)

    tcp_settings = {
        "acceptProxyProtocol": False,
        "header": {"type": "none"},
    }
    stream_settings = StreamSettings(security="reality", network="tcp", tcp_settings=tcp_settings)

    inbound = Inbound(
        enable=True,
        port=443,
        protocol="vless",
        settings=settings,
        stream_settings=stream_settings,
        sniffing=sniffing,
        remark="test3",
    )
    await api.inbound.add(inbound)
