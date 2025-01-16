import json
import logging
import sys
from pathlib import Path

from pythreads.api import API
from pythreads.credentials import Credentials
from pythreads.threads import Threads

LOG = logging.getLogger(__name__)
CREDENTIALS_FILE = "threads_credentials.json"


# Private functions
def _save_credentials(credentials: Credentials) -> None:
    """Saves the Credentials object to a local JSON file."""
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        f.write(credentials.to_json())


def _load_credentials(creds_file=CREDENTIALS_FILE) -> Credentials:
    """Loads the Credentials object from the local JSON file."""
    with open(CREDENTIALS_FILE if creds_file is None else creds_file, "r", encoding="utf-8") as f:
        data = f.read()
    return Credentials.from_json(data)


async def _post_text(text: str, creds_file=None) -> bool:
    """
    Posts a text-only Thread using an `API` instance created with stored credentials.

    This usage follows the pattern from:
    https://github.com/dmytrostriletskyi/pythreads/blob/main/examples/pythreads_example.py
    """
    try:
        credentials = _load_credentials(creds_file)
    except FileNotFoundError:
        LOG.error("No credentials file found. Run this script with `authorize` first.")
        sys.exit(1)

    # Use an async context manager so pythreads can manage its aiohttp.ClientSession
    async with API(credentials=credentials) as api:
        try:
            # 1. Create a container for a text-only post by passing a dict with "caption"
            container_id = await api.create_container(text=text)
            LOG.debug(f"Created container: {container_id}")

            # 2. Publish the container
            published_id = await api.publish_container(container_id)
            LOG.debug(f"Published container with id: {published_id}")

            LOG.info("Success! Your text post has been published.")
            return True
        except Exception as e:
            LOG.error(f"Failed to post text: {e}")
            return False


# Public function
async def post_to_threads(text: str, creds_file: str) -> bool:
    """Public function to post a text thread."""
    return await _post_text(text, creds_file)


# Private function
def _authorize() -> None:
    """
    Initiates the Threads OAuth flow by printing an authorization URL, then
    reading the redirect URL from the user. Finally, it saves the resulting
    long-lived token as credentials.json.
    """
    auth_url, state_key = Threads.authorization_url()
    print(">>> STEP 1: Copy this URL and open in a browser to authorize:")
    print(auth_url)

    # The user will authorize, and the browser will redirect them to your
    # THREADS_REDIRECT_URI. That redirect will include a code and the same `state`.
    print("\n>>> STEP 2: After authorizing, you will land on your redirect URI.")
    print("           Copy the entire browser URL and paste it below.\n")

    # Let the user paste the redirect URL
    content = json.loads(input("Paste the json from your browser URL: "))

    # Exchange the code for a long-lived access token
    credentials = Threads.complete_authorization(content["redirect_url"], content["state"])
    print("\n[INFO] Credentials obtained:\n", credentials.to_json())

    # Save credentials to file
    _save_credentials(credentials)
    print(f"\n[OK] Credentials saved to {CREDENTIALS_FILE}")


if __name__ == "__main__":
    if not Path(CREDENTIALS_FILE).is_file():
        _authorize()
