# app_core.py
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
import pyttsx3
import commands
import json
import os

# ---------------- VOICE ----------------
engine = pyttsx3.init()
for v in engine.getProperty('voices'):
    if "zira" in v.name.lower():
        engine.setProperty('voice', v.id)
engine.setProperty("rate", 160)

def speak(text):
    if text:
        engine.say(text)
        engine.runAndWait()

# ---------------- CONFIG ----------------
CONFIG_FILE = "config.json"

default_config = {
    "startup_message": True,
    "confirm_on_close": True,
    "chat_bg_color": "#ece5dd",
    "chat_bg_image": ""
}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

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
    except (json.JSONDecodeError, ValueError):
        save_config(default_config)
        return default_config

config = load_config()

# ---------------- SETTINGS WINDOW ----------------
def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("350x250")

    # General Settings
    tk.Label(settings_win, text="General Settings", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
    
    startup_var = tk.BooleanVar(value=config.get("startup_message", True))
    tk.Checkbutton(settings_win, text="Show startup message", variable=startup_var).pack(anchor="w", padx=20)

    close_var = tk.BooleanVar(value=config.get("confirm_on_close", True))
    tk.Checkbutton(settings_win, text="Confirm before closing", variable=close_var).pack(anchor="w", padx=20)

    # Appearance Settings
    tk.Label(settings_win, text="Appearance Settings", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)

    # Change chat background color
    def change_bg_color():
        color = colorchooser.askcolor(title="Select Chat Background Color")[1]
        if color:
            config["chat_bg_color"] = color
            chat_frame.config(bg=color)
            canvas.config(bg=color)
            scrollable_frame.config(bg=color)

    tk.Button(settings_win, text="Change Chat Background Color", command=change_bg_color).pack(anchor="w", padx=20, pady=2)

    # Change wallpaper
    def change_bg_image():
        file_path = filedialog.askopenfilename(title="Select Wallpaper Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            config["chat_bg_image"] = file_path
            if file_path:
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(file_path)
                    img = img.resize((450, 700))
                    bg_img = ImageTk.PhotoImage(img)
                    canvas.create_image(0, 0, image=bg_img, anchor="nw")
                    canvas.bg_image = bg_img  # keep reference
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load image: {e}")

    tk.Button(settings_win, text="Select Wallpaper Image", command=change_bg_image).pack(anchor="w", padx=20, pady=2)

    # Save button
    def save_and_close():
        config["startup_message"] = startup_var.get()
        config["confirm_on_close"] = close_var.get()
        save_config(config)
        settings_win.destroy()

    tk.Button(settings_win, text="Save Settings", command=save_and_close).pack(pady=10)

# ---------------- APP START ----------------
def start():
    global root
    global chat_frame, canvas, scrollable_frame
    root = tk.Tk()
    root.geometry("450x700")
    root.title("Lily AI")

    # ---------------- CHAT AREA ----------------
    chat_frame = tk.Frame(root, bg=config.get("chat_bg_color", "#ece5dd"))
    chat_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(chat_frame, bg=config.get("chat_bg_color", "#ece5dd"), highlightthickness=0)
    scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=config.get("chat_bg_color", "#ece5dd"))

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---------------- SETTINGS BUTTON ----------------
    settings_btn = tk.Button(root, text="⚙️ Settings", command=open_settings)
    settings_btn.place(relx=1.0, x=-10, y=10, anchor="ne")  # top-right corner

    # ---------------- INPUT AREA ----------------
    entry_frame = tk.Frame(root)
    entry_frame.pack(fill="x")

    entry = tk.Entry(entry_frame)
    entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    def add_message(sender, text):
        bubble_color = "#dcf8c6" if sender == "Lily" else "#fff"
        bubble = tk.Label(
            scrollable_frame,
            text=text,
            bg=bubble_color,
            wraplength=300,
            justify="left",
            anchor="w",
            padx=10,
            pady=5
        )
        bubble.pack(
            anchor="w" if sender == "Lily" else "e",
            pady=5,
            padx=10
        )
        if sender == "Lily":
            speak(text)
        canvas.update_idletasks()
        canvas.yview_moveto(1.0)

    def send_command():
        t = entry.get()
        if not t.strip():
            return
        entry.delete(0, tk.END)
        add_message("You", t)
        try:
            response = commands.brain(t)
        except Exception as e:
            response = f"Error: {e}"
        add_message("Lily", response)

    send_btn = tk.Button(entry_frame, text="Send", command=send_command)
    send_btn.pack(side="right", padx=5)

    # ---------------- STARTUP MESSAGE ----------------
    if config.get("startup_message", True):
        add_message("Lily", "Hello! I am Lily. I can open apps, play files, and update myself automatically!")

    # ---------------- CLOSE CONFIRM ----------------
    def on_close():
        if config.get("confirm_on_close", True):
            if messagebox.askokcancel("Quit", "Do you really want to close Lily?"):
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
