import os
import subprocess

# ---------------- OPEN APPS ----------------
def open_app(text):
    text = text.lower()  # make text lowercase for easy matching
    apps = {
        "chrome": ["chrome"],
        "notepad": ["notepad"],
        "calculator": ["calculator","calc"]
    }
    for app, keywords in apps.items():
        for kw in keywords:
            if kw in text and "open" in text:
                subprocess.Popen([app+".exe"])  # Opens the app
                return f"Opening {app}"
    return None

# ---------------- PLAY FILES ----------------
def play_media(text):
    if "play" in text:
        # Remove the word "play" from the text to get the filename
        name = text.replace("play","").strip()
        # Check common folders for files
        paths = [os.getcwd(), os.path.expanduser("~/Music"),
                 os.path.expanduser("~/Videos"), os.path.expanduser("~/Downloads")]
        for path in paths:
            for root, _, files in os.walk(path):
                for f in files:
                    if name.lower() in f.lower():  # match file name
                        os.startfile(os.path.join(root,f))  # Open the file
                        return f"Playing {f}"
        return "File not found"

# ---------------- BRAIN ----------------
def brain(text):
    """
    This function decides what to do based on what you type.
    It first tries open_app, then play_media.
    """
    for func in [open_app, play_media]:
        r = func(text)
        if r is not None:
            return r
    return "I don't understand that command"