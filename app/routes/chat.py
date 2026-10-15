from fastapi import APIRouter
from app.ai.models import models

router = APIRouter()

@router.post("/llm")
def llm_chat(prompt: str):

    gemini_model = models.gemini_llm(prompt)

    return gemini_model

