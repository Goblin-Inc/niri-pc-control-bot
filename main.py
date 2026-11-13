import asyncio
import json
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from modules import system, niri_ipc, presets

CONFIG_PATH = Path("config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

bot = Bot(token=config["bot_token"])
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(system.router)
dp.include_router(niri_ipc.router)
dp.include_router(presets.router)

def get_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📸 Скриншот"), KeyboardButton(text="🪟 Управление окнами")],
            [KeyboardButton(text="🖥️ Рабочие столы"), KeyboardButton(text="🚀 Пресеты и софт")],
            [KeyboardButton(text="🔒 Заблокировать"), KeyboardButton(text="⚡ Выключение")]
        ],
        resize_keyboard=True
    )

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id not in config["allowed_users"]:
        return await message.answer("⛔ Доступ запрещен.")
    
    await message.answer("👋 ПК под управлением. Выберите команду:", reply_markup=get_main_kb())

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
