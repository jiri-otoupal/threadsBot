import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Dict, Tuple

import openai
from openai import OpenAI

from text_constants import role_desc

LOG = logging.getLogger(__name__)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Function to translate text using OpenAI's Chat API
async def generate_posts_batch(text, override_role=None):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": role_desc if override_role is None else override_role},
                {"role": "user", "content": text}
            ],
            temperature=0.75,
        )
    except openai.RateLimitError:
        time.sleep(60)
        return await generate_posts_batch(text)
    try:
        out = json.loads(response.choices[0].message.content)
        LOG.info(f"Generated {len(out)} posts")
        return out
    except Exception as ex:
        LOG.info(f"Failed to parse response from OpenAI {ex}")
        LOG.info(response.choices[0].message.content)
        return []


async def save_batch(name: str, batch: list[Dict]):
    if not batch:
        return
    complete = {"t": time.time(), "posts": batch}
    with open(f"posts-{name}.json", "w", encoding="utf-8") as f:
        json.dump(complete, f, indent=4)


async def get_next_post(name: str) -> Tuple[str, datetime, float] | None:
    # Load the JSON file
    filename = f"posts-{name}.json"
    filepath = Path(filename)
    if not await posts_exist(name):
        raise FileNotFoundError(f"The file {filename} does not exist.")

    with filepath.open("r") as file:
        data = json.load(file)

    # Convert the timestamp to a datetime object
    timestamp = datetime.fromtimestamp(data["t"])

    # Find the post with the highest predicted_reach
    posts = data["posts"]
    if not posts:
        LOG.info("No posts available.")
        return None

    m_p = len(posts) - 1
    highest_post = posts[randint(0, m_p)]

    # Remove the post and its "predicted_reach" key from the list
    posts.remove(highest_post)
    reach = highest_post["predicted_reach"]
    highest_post.pop("predicted_reach", None)

    # Save the updated JSON back to the file
    with filepath.open("w") as file:
        json.dump(data, file, indent=4)

    return highest_post["post"], timestamp, reach


async def posts_exist(name):
    filename = f"posts-{name}.json"
    filepath = Path(filename)
    return filepath.is_file()


if __name__ == "__main__":
    print(get_next_post("ava"))
