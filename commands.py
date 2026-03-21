# commands.py
import os
import platform
import subprocess
import memory

# Map common apps to system commands (Windows examples)
COMMON_APPS = {
    "settings": "ms-settings:",
    "file explorer": "explorer",
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "command prompt": "cmd",
}

def brain(text):
    text = text.lower()

    # ------------------ Memory Commands ------------------
    if text.startswith("remember"):
        try:
            key, value = text.replace("remember", "").strip().split("=", 1)
            memory.remember(key.strip(), value.strip())
            return f"I've remembered {key.strip()}."
        except:
            return "Use format: remember key = value"

    if text.startswith("recall"):
        key = text.replace("recall", "").strip()
        val = memory.recall(key)
        return f"{key} is {val}." if val else f"I don't remember {key}."

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
        # Remove command keyword
        target = text.replace("open", "").replace("play", "").strip()
        if not target:
            return "Please say what to open or play."

        # Check if it's a common app
        if target in COMMON_APPS:
            cmd = COMMON_APPS[target]
            try:
                if platform.system() == "Windows":
                    os.startfile(cmd)  # Windows apps
                else:
                    subprocess.call([cmd])  # macOS/Linux (adjust as needed)
                return f"Opened {target}"
            except Exception as e:
                return f"Failed to open {target}: {e}"

        # Try to open as file path (if user provides path)
        try:
            if platform.system() == "Windows":
                os.startfile(target)
            elif platform.system() == "Darwin":
                subprocess.call(["open", target])
            else:
                subprocess.call(["xdg-open", target])
            return f"Opened {target}"
        except Exception as e:
            return f"Failed to open {target}: {e}"

    # ------------------ Default Response ------------------
    return "I don't understand that command yet."
