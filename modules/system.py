import subprocess
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.screenshot import capture_screenshot, cleanup_screenshot

router = Router()

@router.message(F.text == "📸 Скриншот")
async def handle_screenshot(message: types.Message):
    msg = await message.answer("📸 Снимаю экран...")
    photo = await capture_screenshot()
    if photo:
        await message.answer_photo(photo, caption="🖥️ Текущий экран")
        cleanup_screenshot()
        await msg.delete()
    else:
        await msg.edit_text("❌ Ошибка: проверь, установлен ли `grim`.")

@router.message(F.text == "🔒 Заблокировать")
async def lock_screen(message: types.Message):
    subprocess.Popen(["loginctl", "lock-session"])
    await message.answer("🔒 Сессия заблокирована")

@router.message(F.text == "⚡ Выключение")
async def confirm_shutdown(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Выключить", callback_data="power_off_confirm"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="power_cancel")
        ]
    ])
    await message.answer("⚠️ Выключить ПК?", reply_markup=kb)

@router.callback_query(F.data == "power_off_confirm")
async def execute_shutdown(callback: types.CallbackQuery):
    await callback.message.edit_text("🔌 Выключение...")
    subprocess.run(["systemctl", "poweroff"])

@router.callback_query(F.data == "power_cancel")
async def cancel_shutdown(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Действие отменено")
