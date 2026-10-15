from fastapi import APIRouter

from app.ai.fallry import llm_with_retry_and_fallback

router = APIRouter()

@router.post("/llm")
def llm_chat(prompt: str):
    return llm_with_retry_and_fallback(prompt)
