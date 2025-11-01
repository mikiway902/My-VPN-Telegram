import asyncio
import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from handlers import TgBotActions  # импортируем router из модуля

# Загрузка .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TELEGRAM_TOKEN")
print(env_path)
# Создаем Dispatcher и подключаем router
dp = Dispatcher()
dp.include_router(TgBotActions.router)

# Хендлер команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    kb = [
        [
            KeyboardButton(text="Регистрация"),
            KeyboardButton(text="Установить VPN"),
            KeyboardButton(text="Мои данные"),
            KeyboardButton(text="Удалить информацию"),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer(f"Добрый день, {html.bold(message.from_user.full_name)}!")
    await message.answer("Что бы вы хотели сделать?", reply_markup=keyboard)

# Основная функция запуска бота
async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
