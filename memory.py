import json
import os
import threading
import logging
from datetime import datetime

# =========================
# LOGGING
# =========================

logging.basicConfig(
    filename="lily.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =========================
# FILES
# =========================

MEMORY_FILE = "memory.json"
BACKUP_FILE = "memory_backup.json"

# =========================
# THREAD LOCK
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

                logging.info("Memory loaded successfully.")

        else:

            memory = {}

            save_memory()

    except Exception as e:

        logging.error(f"Failed to load memory: {e}")

        # Attempt recovery from backup
        try:

            if os.path.exists(BACKUP_FILE):

                with open(BACKUP_FILE, "r", encoding="utf-8") as f:

                    memory = json.load(f)

                    logging.info("Recovered memory from backup.")

        except Exception as backup_error:

            logging.error(f"Backup recovery failed: {backup_error}")

            memory = {}

# =========================
# SAVE MEMORY
# =========================

def save_memory():

    with memory_lock:

        try:

            # Backup current file first
            if os.path.exists(MEMORY_FILE):

                with open(MEMORY_FILE, "r", encoding="utf-8") as original:

                    data = original.read()

                with open(BACKUP_FILE, "w", encoding="utf-8") as backup:

                    backup.write(data)

            # Save new memory
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:

                json.dump(memory, f, indent=4)

            logging.info("Memory saved successfully.")

        except Exception as e:

            logging.error(f"Failed to save memory: {e}")

# =========================
# REMEMBER
# =========================

def remember(key, value, category="general"):

    with memory_lock:

        key = str(key).strip().lower()

        memory[key] = {
            "value": str(value).strip(),
            "category": category,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_accessed": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        save_memory()

        logging.info(f"Remembered: {key}")

# =========================
# RECALL
# =========================

def recall(key):

    with memory_lock:

        key = str(key).strip().lower()

        data = memory.get(key)

        if not data:
            return None

        data["last_accessed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_memory()

        return data.get("value")

# =========================
# CLEAR MEMORY
# =========================

def clear_memory(key=None):

    with memory_lock:

        if key:

            key = str(key).strip().lower()

            if key in memory:

                del memory[key]

                logging.info(f"Cleared memory key: {key}")

        else:

            memory.clear()

            logging.info("Cleared all memory.")

        save_memory()

# =========================
# GET ALL MEMORY
# =========================

def get_all_memory():

    return memory

# =========================
# SEARCH MEMORY
# =========================

def search_memory(keyword):

    keyword = keyword.lower()

    results = {}

    for key, value in memory.items():

        if keyword in key.lower() or keyword in str(value).lower():

            results[key] = value

    return results

# =========================
# INITIALIZE
# =========================

load_memory()
