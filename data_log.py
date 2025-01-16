import asyncio
import json
import time
from pathlib import Path

import aiofiles

DATA_FILE = Path("data.json")


async def load_last_posted_time() -> dict:
    """Loads the last posted time and additional data from a JSON file."""
    if not DATA_FILE.exists():
        current_time = time.time()
        await save_last_posted_time(current_time, {})
        return {"last_posted_time": current_time}

    async with aiofiles.open(DATA_FILE, mode="r") as file:
        content = await file.read()
        data = json.loads(content)
    return data


async def save_last_posted_time(timestamp: float, additional_data: dict) -> None:
    """Saves the current timestamp as the last posted time and merges additional data."""
    if DATA_FILE.exists():
        content = await asyncio.to_thread(DATA_FILE.read_text)
        existing_data = json.loads(content)
    else:
        existing_data = {}

    existing_data.update(additional_data)
    existing_data["last_posted_time"] = timestamp
    await asyncio.to_thread(DATA_FILE.write_text, json.dumps(existing_data))
