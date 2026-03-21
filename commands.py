# commands.py
import memory
import os
import subprocess
import platform

def brain(command):
    cmd = command.lower().strip()

    # --- MEMORY / THINKING ---
    if "my name is" in cmd:
        name = cmd.split("my name is")[-1].strip()
        memory.remember("user_name", name)
        return f"Nice to meet you, {name}!"

    if "what is my name" in cmd:
        name = memory.recall("user_name")
        return f"Your name is {name}" if name else "I don't know your name yet."

    if cmd.startswith("remember"):
        try:
            key, value = cmd.split("remember")[-1].strip().split("=")
            key, value = key.strip(), value.strip()
            memory.remember(key, value)
            return f"I will remember {key} = {value}"
        except:
            return "Please use the format: remember key = value"

    if cmd.startswith("recall"):
        key = cmd.split("recall")[-1].strip()
        value = memory.recall(key)
        return f"{key} = {value}" if value else f"I don't remember {key}"

    if cmd in ["clear memory", "reset memory"]:
        memory.clear_memory()
        return "I have cleared all my memory."

    # --- SYSTEM ACTIONS ---

    if cmd.startswith("open "):
        app_name = cmd.split("open")[-1].strip()
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(f'start "" "{app_name}"', shell=True)
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", app_name])
            elif system == "Linux":
                subprocess.Popen([app_name])
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"

    if cmd.startswith("play file "):
        file_path = cmd.split("play file")[-1].strip()
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":
                subprocess.Popen(["open", file_path])
            elif system == "Linux":
                subprocess.Popen(["xdg-open", file_path])
            return f"Playing {file_path}..."
        except Exception as e:
            return f"Failed to play {file_path}: {e}"

    # --- STATIC COMMANDS ---
    commands = {
        "hello": "Hi there! How can I help you today?",
        "joke": "Why did the AI go to school? To improve its byte-size knowledge!",
        "time": "I can't tell the time yet, but I'm learning!"
    }

    return commands.get(cmd, "Sorry, I don't understand that yet.")
