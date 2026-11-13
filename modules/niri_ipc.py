import asyncio
import json
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

async def run_niri_cmd(*args) -> str:
    proc = await asyncio.create_subprocess_exec(
        "niri", "msg", *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode().strip()

# --- ЗАКРЫТИЕ ОКН ---
@router.message(F.text == "🪟 Управление окнами")
async def list_windows_menu(message: types.Message):
    raw_json = await run_niri_cmd("-j", "windows")
    try:
        windows = json.loads(raw_json)
        if not windows:
            return await message.answer("Нет открытых окон.")

        keyboard = []
        for w in windows:
            w_id = w.get("id")
            title = w.get("title", "Без названия")[:22]
            app_id = w.get("app_id", "App")
            keyboard.append([
                InlineKeyboardButton(
                    text=f"❌ {app_id}: {title}",
                    callback_data=f"close_win_{w_id}"
                )
            ])

        kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer("Нажмите на окно, чтобы закрыть его:", reply_markup=kb)
    except Exception as e:
        await message.answer(f"❌ Ошибка IPC Niri: {e}")

@router.callback_query(F.data.startswith("close_win_"))
async def close_window_callback(callback: CallbackQuery):
    win_id = callback.data.split("_")[-1]
    # Фокусируем нужное окно и посылаем сигнал закрытия
    await run_niri_cmd("action", "focus-window", "--id", win_id)
    await run_niri_cmd("action", "close-window")
    await callback.answer("Окно закрыто!")
    await callback.message.edit_text("✅ Окно успешно закрыто.")

# --- РАБОЧИЕ СТОЛЫ ---
@router.message(F.text == "🖥️ Рабочие столы")
async def workspaces_menu(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Вверх (Пред.)", callback_data="ws_up"),
            InlineKeyboardButton(text="Вниз (След.) ➡️", callback_data="ws_down")
        ],
        [
            InlineKeyboardButton(text="1️⃣ Стол 1", callback_data="ws_idx_1"),
            InlineKeyboardButton(text="2️⃣ Стол 2", callback_data="ws_idx_2"),
            InlineKeyboardButton(text="3️⃣ Стол 3", callback_data="ws_idx_3")
        ]
    ])
    await message.answer("Управление рабочими столами:", reply_markup=kb)

@router.callback_query(F.data.startswith("ws_"))
async def switch_workspace(callback: CallbackQuery):
    action = callback.data.replace("ws_", "")
    if action == "up":
        await run_niri_cmd("action", "focus-workspace-up")
    elif action == "down":
        await run_niri_cmd("action", "focus-workspace-down")
    elif action.startswith("idx_"):
        idx = action.split("_")[1]
        await run_niri_cmd("action", "focus-workspace", idx)

    await callback.answer("Стол переключен!")
