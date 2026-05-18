import json
import os
import threading
from datetime import datetime

# =========================
# FILES
# =========================

MEMORY_FILE = "config/memory.json"

# =========================
# LOCK
# =========================

memory_lock = threading.Lock()

# =========================
# MEMORY STORAGE
# =========================

memory = {}

# =========================
# LOAD MEMORY
# =========================

def load_memory():

    global memory

    try:

        if os.path.exists(MEMORY_FILE):

            with open(MEMORY_FILE, "r", encoding="utf-8") as f:

                memory = json.load(f)

        else:

            save_memory()

    except:

        memory = {}

# =========================
# SAVE MEMORY
# =========================

def save_memory():

    with memory_lock:

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:

            json.dump(memory, f, indent=4)

# =========================
# REMEMBER
# =========================

def remember(key, value):

    with memory_lock:

        memory[key] = {
            "value": value,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        save_memory()

# =========================
# RECALL
# =========================

def recall(key):

    data = memory.get(key)

    if data:
        return data.get("value")

    return None

# =========================
# CLEAR MEMORY
# =========================

def clear_memory(key=None):

    with memory_lock:

        if key:

            memory.pop(key, None)

        else:

            memory.clear()

        save_memory()

# =========================
# INIT
# =========================

load_memory()
