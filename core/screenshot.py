import asyncio
from pathlib import Path
from aiogram.types import FSInputFile

TMP_SCREENSHOT = Path("/tmp/bot_screenshot.png")

async def capture_screenshot() -> FSInputFile | None:
    proc = await asyncio.create_subprocess_exec("grim", str(TMP_SCREENSHOT))
    await proc.wait()
    if TMP_SCREENSHOT.exists():
        return FSInputFile(TMP_SCREENSHOT)
    return None

def cleanup_screenshot():
    if TMP_SCREENSHOT.exists():
        TMP_SCREENSHOT.unlink()
