# Niri PC Control Bot

> 🌐 **Language:** **English** | [Русский (README_Ru.md)](README_Ru.md)

A Telegram bot built with **Python (`aiogram 3`)** for remotely managing a Linux desktop and the **Niri (Wayland)** scrollable-tiling compositor via IPC.

## ✨ Features
- 📸 **Instant Screenshots** — captures the screen via `grim` and sends it directly to your Telegram chat.
- 🪟 **Window Management (Niri IPC)** — lists all open windows and lets you close any window via inline buttons (`niri msg -j windows`).
- 🖥️ **Workspace Control** — switch active Niri workspaces remotely via IPC.
- 🚀 **App Presets & Command Runner** — launch predefined application workspaces (e.g., *"Work"*, *"Relax"*) or execute custom commands straight from Telegram.
- 🔒 **Security & Power Management** — lock the current session (`loginctl lock-session`), confirm system shutdown, and restrict access by Telegram user ID (`allowed_users`).

## 🚀 Installation & Usage

1. Clone the repository and create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `config.example.json` to `config.json` and fill in your bot token and Telegram ID:
   ```bash
   cp config.example.json config.json
   ```
3. Start the bot:
   ```bash
   python3 main.py
   ```

## 📄 License
MIT © [Goblin-Inc](https://github.com/Goblin-Inc)
