from google import genai
from groq import Groq
from app.core.config import settings
from app.ai.prompts.gemini_prompt import SYSTEM_PROMPT



class Models:
    def __init__(self):
        gemini_client = Groq(api_key= settings.GROQ_API_KEY)
        groq_client = genai.Client(api_key = settings.GEMINI_API_KEY)

    def gemini_llm(prompt: str):

        response = client.interactions.create(
            model= "gemini-3.5-flash-lite",
            system_instruction= SYSTEM_PROMPT,
            input = prompt
        )

        return response.output_text


    def groq_llm(prompt: str):

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain the importance of fast language models",
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        return chat_completion.choices[0].message.content

models = Models()

