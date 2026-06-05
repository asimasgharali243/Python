import logging
from google import genai
from config import GEMINI_API_KEY, MODEL_NAME

logging.basicConfig(filename="logs/chatbot.log", level=logging.INFO)

SYSTEM_PROMPT = """
You are a professional health information assistant.
Rules:
- Educational information only
- No diagnosis
- No prescriptions
- Always suggest doctor consultation
- Warn for serious symptoms
"""

client = genai.Client(api_key=GEMINI_API_KEY)


def get_response(query, history):
    try:
        # Convert history to SIMPLE text (NOT structured format)
        chat_history = ""

        for m in history:
            chat_history += f"{m['role']}: {m['content']}\n"

        final_prompt = f"""
{SYSTEM_PROMPT}

Chat history:
{chat_history}

User: {query}
Assistant:
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=final_prompt
        )

        return response.text

    except Exception as e:
        logging.exception(e)
        return f"Error: {str(e)}"