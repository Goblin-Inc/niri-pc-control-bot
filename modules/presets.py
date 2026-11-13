import json
import subprocess
from pathlib import Path
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()
CONFIG_PATH = Path("config.json")

class AddPreset(StatesGroup):
    name = State()
    apps = State()

class LaunchApp(StatesGroup):
    app_cmd = State()

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

@router.message(F.text == "🚀 Пресеты и софт")
async def presets_menu(message: types.Message):
    cfg = load_config()
    presets = cfg.get("presets", {})

    keyboard = []
    for name, p_data in presets.items():
        title = p_data.get("title", name)
        keyboard.append([InlineKeyboardButton(text=f"▶️ {title}", callback_data=f"run_preset_{name}")])

    keyboard.append([InlineKeyboardButton(text="⚡ Запустить команду/софт", callback_data="run_custom_app")])
    keyboard.append([InlineKeyboardButton(text="➕ Создать пресет", callback_data="add_preset_start")])

    kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer("Управление приложениями и пресетами:", reply_markup=kb)

@router.callback_query(F.data.startswith("run_preset_"))
async def run_preset(callback: CallbackQuery):
    preset_key = callback.data.replace("run_preset_", "")
    cfg = load_config()
    preset = cfg.get("presets", {}).get(preset_key)

    if not preset:
        return await callback.answer("Пресет не найден!", show_alert=True)

    for app in preset.get("apps", []):
        subprocess.Popen(app, shell=True)

    await callback.answer(f"Запущен: {preset.get('title', preset_key)}")

# --- ЗАПУСК ОДНОЙ КОМАНДЫ ---
@router.callback_query(F.data == "run_custom_app")
async def start_custom_app(callback: CallbackQuery, state: FSMContext):
    await state.set_state(LaunchApp.app_cmd)
    await callback.message.answer("Введите название программы или команду для запуска (например: `firefox`, `kitty`, `pavucontrol`):")
    await callback.answer()

@router.message(LaunchApp.app_cmd)
async def execute_custom_app(message: types.Message, state: FSMContext):
    cmd = message.text.strip()
    try:
        subprocess.Popen(cmd, shell=True)
        await message.answer(f"🚀 Команда `{cmd}` запущена!")
    except Exception as e:
        await message.answer(f"❌ Ошибка запуска: {e}")
    await state.clear()

# --- СОЗДАНИЕ ПРЕСЕТА ---
@router.callback_query(F.data == "add_preset_start")
async def add_preset_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPreset.name)
    await callback.message.answer("Введите название нового пресета (например: `Игры` или `Dev`):")
    await callback.answer()

@router.message(AddPreset.name)
async def add_preset_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddPreset.apps)
    await message.answer("Введите команды/программы через запятую (например: `vscodium, firefox, telegram-desktop`):")

@router.message(AddPreset.apps)
async def add_preset_apps(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    apps = [a.strip() for a in message.text.split(",") if a.strip()]

    cfg = load_config()
    if "presets" not in cfg:
        cfg["presets"] = {}

    preset_key = name.lower().replace(" ", "_")
    cfg["presets"][preset_key] = {
        "title": name,
        "apps": apps
    }
    save_config(cfg)

    await message.answer(f"✅ Пресет **{name}** сохранен!")
    await state.clear()

