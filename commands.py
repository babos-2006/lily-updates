import os
import platform
import subprocess
import logging
import re

import memory

# =========================
# LOGGING
# =========================

logging.basicConfig(
    filename="lily.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =========================
# COMMON APPS
# =========================

COMMON_APPS = {
    "settings": "ms-settings:",
    "file explorer": "explorer",
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "command prompt": "cmd",
    "task manager": "taskmgr",
    "control panel": "control",
}

# =========================
# HELPERS
# =========================

def clean_text(text):
    return text.lower().strip()

def contains_words(text, words):
    return any(word in text for word in words)

# =========================
# MEMORY COMMANDS
# =========================

def handle_memory_commands(text):

    # Remember
    if text.startswith("remember"):

        try:
            content = text.replace("remember", "").strip()

            key, value = content.split("=", 1)

            key = key.strip()
            value = value.strip()

            memory.remember(key, value)

            logging.info(f"Memory saved: {key}")

            return f"I've remembered {key}."

        except Exception as e:

            logging.error(f"Memory save error: {e}")

            return "Use format: remember key = value"

    # Recall
    if text.startswith("recall"):

        key = text.replace("recall", "").strip()

        val = memory.recall(key)

        if val:
            return f"{key} is {val}."

        return f"I don't remember {key}."

    # Clear Memory
    if text.startswith("clear memory"):

        key = text.replace("clear memory", "").strip()

        if key:
            memory.clear_memory(key)
            return f"Cleared memory for {key}."

        memory.clear_memory()

        return "All memory cleared."

    return None

# =========================
# OPEN COMMANDS
# =========================

def handle_open_commands(text):

    patterns = [
        r"open (.+)",
        r"play (.+)",
        r"launch (.+)",
        r"start (.+)"
    ]

    target = None

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            target = match.group(1).strip()
            break

    if not target:
        return None

    # =========================
    # COMMON APPS
    # =========================

    if target in COMMON_APPS:

        cmd = COMMON_APPS[target]

        try:

            if platform.system() == "Windows":
                os.startfile(cmd)

            else:
                subprocess.call([cmd])

            logging.info(f"Opened app: {target}")

            return f"Opened {target}."

        except Exception as e:

            logging.error(f"Failed to open {target}: {e}")

            return f"Failed to open {target}."

    # =========================
    # FILES / PATHS
    # =========================

    try:

        if os.path.exists(target):

            if platform.system() == "Windows":
                os.startfile(target)

            elif platform.system() == "Darwin":
                subprocess.call(["open", target])

            else:
                subprocess.call(["xdg-open", target])

            logging.info(f"Opened file/path: {target}")

            return f"Opened {target}"

        else:
            return f"{target} does not exist."

    except Exception as e:

        logging.error(f"Open path error: {e}")

        return f"Failed to open {target}"

# =========================
# BASIC CHAT RESPONSES
# =========================

def handle_small_talk(text):

    greetings = ["hello", "hi", "hey"]

    if contains_words(text, greetings):
        return "Hello! How can I help you today?"

    if "how are you" in text:
        return "I'm functioning perfectly."

    if "your name" in text:
        return "My name is Lily AI."

    return None

# =========================
# MAIN BRAIN
# =========================

def brain(text):

    text = clean_text(text)

    logging.info(f"User Input: {text}")

    # =========================
    # MEMORY
    # =========================

    response = handle_memory_commands(text)

    if response:
        return response

    # =========================
    # OPEN COMMANDS
    # =========================

    response = handle_open_commands(text)

    if response:
        return response

    # =========================
    # SMALL TALK
    # =========================

    response = handle_small_talk(text)

    if response:
        return response

    # =========================
    # FALLBACK
    # =========================

    logging.warning(f"Unknown command: {text}")

    return (
        "I don't understand that yet. "
        "Future versions of Lily will support AI conversation."
    )
