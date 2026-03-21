# memory.py
import json
import os

# File to store persistent memory
MEMORY_FILE = "memory.json"
memory = {}

# Load memory on startup
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except json.JSONDecodeError:
        memory = {}
else:
    # If the file doesn't exist, create an empty one
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# Save memory to disk
def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

# Remember a key-value pair
def remember(key, value):
    key = str(key).strip()
    value = str(value).strip()
    memory[key] = value
    save_memory()

# Recall a value by key
def recall(key):
    return memory.get(str(key).strip(), None)

# Clear memory
# If key is provided, remove that entry; otherwise, clear all memory
def clear_memory(key=None):
    if key:
        memory.pop(str(key).strip(), None)
    else:
        memory.clear()
    save_memory()
