# Niri PC Control Bot

Telegram-бот на **Python (`aiogram 3`)** для удалённого управления Linux-системой и композитным оконным менеджером **Niri (Wayland)** через IPC.

## ✨ Возможности
- 📸 **Скриншот экрана** — мгновенный снимок экрана через `grim` и отправка в чат.
- 🪟 **Управление окнами (Niri IPC)** — просмотр открытых окон и закрытие любого окна по клику на inline-кнопку (`niri msg -j windows`).
- 🖥️ **Управление рабочими столами** — переключение воркспейсов через IPC Niri.
- 🚀 **Пресеты и запуск софта** — запуск заранее настроенных наборов программ (например, «Работа», «Отдых») или произвольных команд прямо из Telegram.
- 🔒 **Безопасность и питание** — блокировка сессии (`loginctl lock-session`), подтверждение выключения ПК и фильтрация по Telegram ID (`allowed_users`).

## 🚀 Установка и запуск

1. Клонируйте репозиторий и создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Скопируйте `config.example.json` в `config.json` и укажите ваш токен бота и Telegram ID:
   ```bash
   cp config.example.json config.json
   ```
3. Запустите бота:
   ```bash
   python3 main.py
   ```
