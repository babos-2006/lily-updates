import logging
import google.generativeai as genai

# =========================
# API CONFIG
# =========================

API_KEY = "YOUR_API_KEY_HERE"

genai.configure(api_key=API_KEY)

# =========================
# MODEL SETUP
# =========================

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# CHAT HISTORY
# =========================

conversation_history = []

# =========================
# SYSTEM PERSONALITY
# =========================

SYSTEM_PROMPT = """
You are Lily AI.

You are a smart desktop AI assistant.
You are friendly, helpful, intelligent, and concise.

You help users with:
- conversations
- productivity
- learning
- computer tasks
- explanations
- problem solving

Keep responses natural and conversational.
Avoid overly long answers unless necessary.
"""

# =========================
# BUILD CONTEXT
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
# MAIN AI FUNCTION
# =========================

def ask_gemini(user_message):

    try:

        # Store user message
        conversation_history.append({
            "role": "User",
            "content": user_message
        })

        # Build contextual prompt
        prompt = build_prompt(user_message)

        # Generate response
        response = model.generate_content(prompt)

        if response.text:

            ai_response = response.text.strip()

            # Store AI response
            conversation_history.append({
                "role": "Lily",
                "content": ai_response
            })

            return ai_response

        return "I couldn't generate a response."

    except Exception as e:

        logging.error(f"Gemini Error: {e}")

        return f"AI Error: {e}"

# =========================
# CLEAR CHAT MEMORY
# =========================

def clear_conversation():

    conversation_history.clear()

# =========================
# GET CHAT HISTORY
# =========================

def get_history():

    return conversation_history
