import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import threading
import json
import os
import pyttsx3

from core import commands

# =========================
# CONFIG
# =========================

CONFIG_FILE = "config/config.json"

DEFAULT_CONFIG = {
    "voice_enabled": True,
    "startup_message": True,
    "confirm_on_close": True,
    "chat_bg": "#1e1e1e",
    "chat_fg": "white"
}

# =========================
# LOAD CONFIG
# =========================

def load_config():

    if not os.path.exists(CONFIG_FILE):

        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

        return DEFAULT_CONFIG

    try:

        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    except:

        return DEFAULT_CONFIG

config = load_config()

# =========================
# VOICE ENGINE
# =========================

engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:

    print(voice.name)

    if "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty("rate", 145)
engine.setProperty("volume", 1.0)

# =========================
# SPEAK
# =========================

def speak(text):

    if not config.get("voice_enabled", True):
        return

    def run():

        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run, daemon=True).start()

# =========================
# APP CLASS
# =========================

class LilyApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Lily AI")

        self.root.geometry("500x750")

        self.setup_ui()

        if config.get("startup_message", True):

            self.add_message(
                "Lily",
                "Hello! I am Lily AI."
            )

    # =========================
    # UI
    # =========================

    def setup_ui(self):

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

        self.chat_area = ScrolledText(
            self.root,
            wrap="word",
            font=("Arial", 11),
            bg=config.get("chat_bg"),
            fg=config.get("chat_fg"),
            state="disabled"
        )

        self.chat_area.pack(fill="both", expand=True, padx=5, pady=5)

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
    # ADD MESSAGE
    # =========================

    def add_message(self, sender, text):

        self.chat_area.config(state="normal")

        self.chat_area.insert(
            tk.END,
            f"\n{sender}: {text}\n"
        )

        self.chat_area.config(state="disabled")

        self.chat_area.see(tk.END)

        if sender == "Lily":
            speak(text)

    # =========================
    # SEND COMMAND
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

    # =========================
    # PROCESS COMMAND
    # =========================

    def process_command(self, text):

        try:

            response = commands.brain(text)

        except Exception as e:

            response = f"Error: {e}"

        self.add_message("Lily", response)

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
