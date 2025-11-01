from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

from handlers.DataBaseLib import add_user_db, show_user_db

# Загрузка .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
router = Router()

class RegistrationForm(StatesGroup):
    email = State()

@router.message(F.text == "Регистрация")
async def start_registration(message: types.Message, state: FSMContext):
    sender_id = message.from_user.id
    await state.update_data(sender_id=sender_id)
    await message.answer("Введите ваш email:")
    await state.set_state(RegistrationForm.email)

@router.message(RegistrationForm.email)
async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    sender_id = data["sender_id"]
    email = data["email"]

    await add_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id, email)
    await message.answer(f"Email {email} сохранён ✅")
    await state.clear()

@router.message(F.text == "Мои данные")
async def return_user_data(message: types.Message):
    sender_id = message.from_user.id
    user = await show_user_db(POSTGRES_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, sender_id)

    if user:
        user_text = "\n".join(f"{k}: {v}" for k, v in user.items())
        await message.answer(f"Ваши данные:\n\n{user_text}")
    else:
        await message.answer("Пользователь не найден 😢")
