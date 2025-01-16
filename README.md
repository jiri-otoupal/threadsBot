# Threads Bot

This repository contains a bot designed to automatically post content to Threads. The bot operates using a modular structure with asynchronous
capabilities, making it efficient and extensible.

---

## Features

- **Automatic Post Scheduling:** Ensures minimum intervals between posts to avoid spam.
- **Dynamic Post Generation:** Generates batches of posts based on a role description.
- **Customizable Post Frequency:** Specify the frequency of posts in seconds via command-line options.
- **Progress Tracking:** Displays progress until the next post using a CLI progress bar.
- **Error Handling:** Handles file and configuration errors gracefully.
- **Asynchronous Architecture:** Utilizes asyncio for efficient and scalable operations.

---

## Requirements

- Python 3.7 or higher
- Dependencies specified in `requirements.txt`
- `.env` file for environment-specific configuration

---

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create openssl certs for https

```
# Generate a private key
openssl genpkey -algorithm RSA -out threads.key -pkeyopt rsa_keygen_bits:2048

# Generate a certificate signing request (CSR)
openssl req -new -key threads.key -out threads.csr

# Generate a self-signed certificate valid for 1 year
openssl x509 -req -days 365 -in threads.csr -signkey threads.key -out threads.crt
```

3. Create a Threads app in Meta
4. Create a `.env` file for storing sensitive or environment-specific data.

```
Example:

THREADS_APP_ID=123123123
THREADS_API_SECRET=SomethingSecret
THREADS_SSL_CERT_FILEPATH="threads.crt"
THREADS_SSL_KEY_FILEPATH="threads.key"
# You need this page to only capture the threads post callback and copy paste this into the script if asked for it
THREADS_REDIRECT_URI="https://your-callback-url/callback"
OPENAI_API_KEY="sk-supersecretopenai-key-which-will-be-used-for-requests"
```

---

## Usage

Run the bot using the following command:

```bash
python bot.py <bot_name> [OPTIONS]
```

### Arguments:

- `<bot_name>`: The unique name of the bot (required).

### Options:

- `-r, --role-txt-path`: Path to a file containing a role description for generating posts (optional).
- `-c, --creds-file-path`: Path to a credentials file for authentication (optional).
- `-f, --post-frequency`: Post frequency in seconds (optional, defaults to 7200 seconds).

### Example:

```bash
python bot.py "MyThreadsBot" -r "role_description.txt" -c "creds.json" -f 3600
```

---

## Key Components

### 1. `main_func`

The entry point of the bot. Handles command-line arguments, reads optional files, and initializes the main asynchronous function.

### 2. `main`

The core loop of the bot:

- Checks for existing posts.
- Generates new posts if none are available.
- Schedules and publishes posts while ensuring proper intervals.

### 3. `api.py`

Handles the API communication for posting content to Threads.

### 4. `fetcher.py`

Manages post generation, saving, and retrieval.

### 5. `data_log.py`

Handles loading and saving the last posted time for ensuring intervals between posts.

### 6. `logging_setup.py`

Sets up structured logging for monitoring and debugging.

### 7. `text_constants.py`

Sets up model behaviour and role

---

## Configuration

### Logging

Logging is configured in `logging_setup.py` to ensure all activities are recorded. Modify the logging level and output format as needed.

### Minimum Timespan

The default interval between posts is set in the script:

```python
MINIMUM_TIMESPAN_BETWEEN_POSTS = 60 * 60 * 2  # 2 hours in seconds
```

You can override this using the `-f` or `--post-frequency` command-line option.

---

## Development

To contribute or modify the bot:

1. Create a new branch:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Make changes and test locally:
   ```bash
   python bot.py <bot_name> [OPTIONS]
   ```

3. Submit a pull request to the `main` branch.

---

## License

This project is licensed under the specific License. See the `LICENSE` file for details.

---

Did you find it useful?
<br>
<br>
Please support my work here
<br>
<a href="https://www.buymeacoffee.com/jiriotoupal" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me a Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>