import json
from pathlib import Path
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

CONFIG_PATH = Path(__file__).parent.parent / "config.json"

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Файл конфигурации не найден: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

class AdminFilter(BaseFilter):
    """Фильтр доступа: пропускает только пользователей из allowed_users."""
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        config = load_config()
        allowed_users = config.get("allowed_users", [])
        return event.from_user.id in allowed_users
