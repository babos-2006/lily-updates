import os
import platform
import subprocess
import re

from core import memory
from core import ai_engine

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
    "task manager": "taskmgr"
}

# =========================
# CLEAN TEXT
# =========================

def clean_text(text):
    return text.lower().strip()

# =========================
# MEMORY COMMANDS
# =========================

def handle_memory_commands(text):

    if text.startswith("remember"):

        try:

            content = text.replace("remember", "").strip()

            key, value = content.split("=", 1)

            memory.remember(key.strip(), value.strip())

            return f"I've remembered {key.strip()}."

        except:

            return "Use format: remember key = value"

    if text.startswith("recall"):

        key = text.replace("recall", "").strip()

        val = memory.recall(key)

        if val:
            return f"{key} is {val}."

        return f"I don't remember {key}."

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

    if target in COMMON_APPS:

        cmd = COMMON_APPS[target]

        try:

            if platform.system() == "Windows":
                os.startfile(cmd)
            else:
                subprocess.call([cmd])

            return f"Opened {target}."

        except Exception as e:

            return f"Failed to open {target}: {e}"

    return None

# =========================
# MAIN BRAIN
# =========================

def brain(text):

    text = clean_text(text)

    response = handle_memory_commands(text)

    if response:
        return response

    response = handle_open_commands(text)

    if response:
        return response

    return ai_engine.ask_gemini(text)
