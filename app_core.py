import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
from tkinter.scrolledtext import ScrolledText

import threading
import logging
import json
import os
import time

import pyttsx3
import commands

# =========================
# LOGGING
# =========================

logging.basicConfig(
    filename="lily.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =========================
# VOICE ENGINE
# =========================

engine = pyttsx3.init()

for voice in engine.getProperty('voices'):
    if "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)

engine.setProperty("rate", 160)

def speak(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logging.error(f"Speech Error: {e}")

    threading.Thread(target=run, daemon=True).start()

# =========================
# CONFIG
# =========================

CONFIG_FILE = "config.json"

default_config = {
    "startup_message": True,
    "confirm_on_close": True,
    "chat_bg_color": "#ece5dd",
    "chat_fg_color": "#000000",
    "voice_enabled": True,
    "window_width": 500,
    "window_height": 750
}

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=4)

    except Exception as e:
        logging.error(f"Failed to save config: {e}")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(default_config)
        return default_config

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        for key in default_config:
            if key not in data:
                data[key] = default_config[key]

        return data

    except Exception as e:
        logging.error(f"Config load failed: {e}")
        save_config(default_config)
        return default_config

config = load_config()

# =========================
# MAIN APP
# =========================

class LilyApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Lily AI")

        width = config.get("window_width", 500)
        height = config.get("window_height", 750)

        self.root.geometry(f"{width}x{height}")

        self.setup_ui()

        if config.get("startup_message", True):
            self.add_message(
                "Lily",
                "Hello! I am Lily AI. How can I help you today?"
            )

    # =========================
    # UI
    # =========================

    def setup_ui(self):

        # Top Bar
        top_frame = tk.Frame(self.root, bg="#202123", height=50)
        top_frame.pack(fill="x")

        title = tk.Label(
            top_frame,
            text="Lily AI",
            bg="#202123",
            fg="white",
            font=("Arial", 14, "bold")
        )
        title.pack(side="left", padx=10, pady=10)

        settings_btn = tk.Button(
            top_frame,
            text="⚙",
            command=self.open_settings
        )
        settings_btn.pack(side="right", padx=10)

        # Chat Area
        self.chat_area = ScrolledText(
            self.root,
            wrap="word",
            font=("Arial", 11),
            bg=config.get("chat_bg_color"),
            fg=config.get("chat_fg_color"),
            state="disabled"
        )

        self.chat_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Input Area
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x")

        self.entry = tk.Entry(
            bottom_frame,
            font=("Arial", 11)
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=5
        )

        self.entry.bind("<Return>", lambda e: self.send_command())

        send_btn = tk.Button(
            bottom_frame,
            text="Send",
            command=self.send_command
        )

        send_btn.pack(side="right", padx=5)

    # =========================
    # MESSAGES
    # =========================

    def add_message(self, sender, text):

        timestamp = time.strftime("%H:%M")

        self.chat_area.config(state="normal")

        self.chat_area.insert(
            tk.END,
            f"\n[{timestamp}] {sender}: {text}\n"
        )

        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)

        if sender == "Lily" and config.get("voice_enabled", True):
            speak(text)

    # =========================
    # COMMAND PROCESSING
    # =========================

    def send_command(self):

        text = self.entry.get().strip()

        if not text:
            return

        self.entry.delete(0, tk.END)

        self.add_message("You", text)

        threading.Thread(
            target=self.process_command,
            args=(text,),
            daemon=True
        ).start()

    def process_command(self, text):

        self.add_message("Lily", "Thinking...")

        try:
            response = commands.brain(text)

        except Exception as e:
            logging.error(f"Command Error: {e}")
            response = f"Error: {e}"

        self.add_message("Lily", response)

    # =========================
    # SETTINGS
    # =========================

    def open_settings(self):

        settings = tk.Toplevel(self.root)

        settings.title("Settings")
        settings.geometry("350x300")

        voice_var = tk.BooleanVar(
            value=config.get("voice_enabled", True)
        )

        startup_var = tk.BooleanVar(
            value=config.get("startup_message", True)
        )

        close_var = tk.BooleanVar(
            value=config.get("confirm_on_close", True)
        )

        tk.Checkbutton(
            settings,
            text="Enable Voice",
            variable=voice_var
        ).pack(anchor="w", padx=20, pady=5)

        tk.Checkbutton(
            settings,
            text="Startup Message",
            variable=startup_var
        ).pack(anchor="w", padx=20, pady=5)

        tk.Checkbutton(
            settings,
            text="Confirm Before Close",
            variable=close_var
        ).pack(anchor="w", padx=20, pady=5)

        def change_bg():

            color = colorchooser.askcolor()[1]

            if color:
                config["chat_bg_color"] = color
                self.chat_area.config(bg=color)

        tk.Button(
            settings,
            text="Change Chat Background",
            command=change_bg
        ).pack(pady=10)

        def save():

            config["voice_enabled"] = voice_var.get()
            config["startup_message"] = startup_var.get()
            config["confirm_on_close"] = close_var.get()

            save_config(config)

            settings.destroy()

        tk.Button(
            settings,
            text="Save Settings",
            command=save
        ).pack(pady=15)

    # =========================
    # CLOSE EVENT
    # =========================

    def on_close(self):

        if config.get("confirm_on_close", True):

            if not messagebox.askokcancel(
                "Quit",
                "Close Lily AI?"
            ):
                return

        self.root.destroy()

# =========================
# START APP
# =========================

def start():

    root = tk.Tk()

    app = LilyApp(root)

    root.protocol("WM_DELETE_WINDOW", app.on_close)

    root.mainloop()

if __name__ == "__main__":
    start()
