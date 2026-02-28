import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import Database
import os
from dotenv import load_dotenv

# Загружаем настройки из .env файла
load_dotenv()

# Настройка логирования (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Берём токен и URL из .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

# Проверяем, что токен есть
if not BOT_TOKEN:
    raise ValueError("Нет токена в .env файле!")
if not WEBAPP_URL:
    raise ValueError("Нет URL в .env файле!")

# Создаём бота и базу данных
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """Когда пользователь пишет /start"""
    user = message.from_user
    
    # Сохраняем или получаем пользователя из базы
    db_user = db.get_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )
    
    # Создаём кнопку для открытия Mini App
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🚀 Открыть игру",
        web_app=WebAppInfo(url=WEBAPP_URL)
    ))
    
    # Отправляем приветствие
    await message.answer(
        f"👋 Привет, {user.first_name}!\n\n"
        f"🎮 Добро пожаловать в игру про покемонов!\n"
        f"📊 Твой баланс: {db_user['pokemon_balance']} покемонов\n"
        f"⛏️ Доход в час: {db_user['pokemon_per_hour']}\n\n"
        f"Нажми кнопку, чтобы открыть игру:",
        reply_markup=builder.as_markup()
    )

@dp.message()
async def handle_web_app_data(message: types.Message):
    """Когда приходят данные из Mini App"""
    if message.web_app_data:
        data = message.web_app_data.data
        await message.answer(f"✅ Получены данные: {data}")

async def main():
    """Запуск бота"""
    print("🚀 Бот запускается...")
    print(f"🤖 Токен: {BOT_TOKEN[:10]}...")
    print(f"🌐 URL игры: {WEBAPP_URL}")
    
    # Удаляем старые данные и запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())