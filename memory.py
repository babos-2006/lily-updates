import json
import os

MEMORY_FILE = "memory.json"
memory = {}

# --- LOAD MEMORY ON STARTUP ---
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except:
        memory = {}

# --- MEMORY FUNCTIONS ---
def save_memory():
    """Save memory to file"""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

def remember(key, value):
    """Store a value in memory and save"""
    memory[key] = value
    save_memory()

def recall(key):
    """Retrieve a value from memory"""
    return memory.get(key, None)

def clear_memory(key=None):
    """Clear specific key or all memory and save"""
    if key:
        memory.pop(key, None)
    else:
        memory.clear()
    save_memory()
