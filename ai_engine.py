import logging
import google.generativeai as genai

# =========================
# GEMINI CONFIG
# =========================

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# =========================
# SETUP
# =========================

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

# =========================
# MEMORY
# =========================

conversation_history = []

# =========================
# PERSONALITY
# =========================

SYSTEM_PROMPT = """
You are Lily AI.

You are a smart desktop assistant.
You are friendly, intelligent, and concise.

You help users with:
- productivity
- explanations
- coding
- learning
- conversations
- desktop assistance

Respond naturally.
"""

# =========================
# BUILD PROMPT
# =========================

def build_prompt(user_message):

    history_text = ""

    for msg in conversation_history[-10:]:
        history_text += f"{msg['role']}: {msg['content']}\n"

    final_prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{history_text}

User: {user_message}

Lily:
"""

    return final_prompt

# =========================
# ASK GEMINI
# =========================

def ask_gemini(user_message):

    try:

        conversation_history.append({
            "role": "User",
            "content": user_message
        })

        prompt = build_prompt(user_message)

        response = model.generate_content(prompt)

        if response.text:

            ai_response = response.text.strip()

            conversation_history.append({
                "role": "Lily",
                "content": ai_response
            })

            return ai_response

        return "I couldn't generate a response."

    except Exception as e:

        logging.error(f"Gemini Error: {e}")

        return f"AI Error: {e}"
