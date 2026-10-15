from pathlib import Path

from google import genai
from google.genai import types
from groq import Groq

from app.core.config import settings


CHARACTER_PROMPT_PATH = Path(__file__).parent / "prompts" / "character.md"
SYSTEM_PROMPT = CHARACTER_PROMPT_PATH.read_text(encoding="utf-8")


class Models:
    def __init__(self):
        self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)

    def gemini_llm(self, prompt: str):
        response = self.gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )

        return response.text

    def groq_llm(self, prompt: str):
        chat_completion = self.groq_client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return chat_completion.choices[0].message.content

models = Models()
