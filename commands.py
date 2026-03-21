# commands.py
import os
import platform
import subprocess
import memory

def brain(text):
    text = text.lower()

    # ------------------ Memory Commands ------------------
    if text.startswith("remember"):
        try:
            key, value = text.replace("remember", "").strip().split("=", 1)
            memory.remember(key.strip(), value.strip())
            return f"I've remembered {key.strip()}."
        except:
            return "Please use format: remember key = value"

    if text.startswith("recall"):
        key = text.replace("recall", "").strip()
        val = memory.recall(key)
        if val:
            return f"{key} is {val}."
        else:
            return f"I don't remember {key}."

    if text.startswith("clear memory"):
        key = text.replace("clear memory", "").strip()
        if key:
            memory.clear_memory(key)
            return f"I've cleared memory for {key}."
        else:
            memory.clear_memory()
            return "I've cleared all memory."

    # ------------------ Open Apps or Files ------------------
    if text.startswith("open ") or text.startswith("play "):
        # Remove the command keyword
        path = text.replace("open", "").replace("play", "").strip()
        if not path:
            return "Please provide a file or app to open."
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", path])
            else:  # Linux
                subprocess.call(["xdg-open", path])
            return f"Opened {path}"
        except Exception as e:
            return f"Failed to open {path}: {e}"

    # ------------------ Default Response ------------------
    return "I don't understand that command yet."
