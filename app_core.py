
# app_core.py

import tkinter as tk
import pyttsx3
import commands

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

# ---------------- APP START FUNCTION ----------------
def start():
    root = tk.Tk()
    root.geometry("450x700")
    root.title("Lily AI")

    # ---------------- CHAT AREA ----------------
    chat_frame = tk.Frame(root, bg="#ece5dd")
    chat_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(chat_frame, bg="#ece5dd", highlightthickness=0)
    scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ece5dd")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---------------- INPUT AREA ----------------
    entry_frame = tk.Frame(root)
    entry_frame.pack(fill="x")

    entry = tk.Entry(entry_frame)
    entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    # ---------------- MESSAGE FUNCTION ----------------
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

    # ---------------- SEND FUNCTION ----------------
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

    # ---------------- START MESSAGE ----------------
    add_message("Lily", "Hello! I am Lily. I update myself automatically 🚀")

    root.mainloop()
