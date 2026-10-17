from google import genai
from groq import Groq
from app.core.config import settings
from app.ai.prompts.gemini_prompt import SYSTEM_PROMPT



class Models:
    def __init__(self):
        self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)

        self.system_prompt = SYSTEM_PROMPT

    async def gemini_llm(self, prompt: str):
        response = self.gemini_client.interactions.create(
            model = "gemini-3.5-flash-lite",
            system_instruction = self.system_prompt,
            input = prompt,
            stream = True
        )

        collected_chunks = []
        for event in response:
            if getattr(event, "event_type", None) == "step.delta":
                if getattr(event.delta, "type", None) == "text":
                    collected_chunks.append(event.delta.text)

        if collected_chunks:
            return "".join(collected_chunks)

        return getattr(response, "output_text", "")

    async def groq_llm(self, prompt: str):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ] if self.system_prompt else [{"role": "user", "content": prompt}]

        chat_completion = self.groq_client.chat.completions.create(
            messages = messages,
            model = "openai/gpt-oss-20b",
            stream = True
        )

        collected_chunks = []
        for chunk in chat_completion:
            if chunk.choices and chunk.choices[0].delta:
                content = chunk.choices[0].delta.content
                if content:
                    collected_chunks.append(content)

        return "".join(collected_chunks)

    def fallback_chain(self):
       
        return [
            ("Google Gemini", self.gemini_llm),
            ("Groq", self.groq_llm)
        ]

    
models = Models()

