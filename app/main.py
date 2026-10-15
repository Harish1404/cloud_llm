from fastapi import FastAPI
from app.routes import chat

app = FastAPI()

@app.get("/")
def landing_page():

    return {
        "message": "Go to docs"
    }

@app.get("/health")
def health():
    return {
        "status": "working"
    }
    
@app.get("/models_list")
def models_list():
    return {
        "models": ["gemini", "groq"]
    }

app.include_router(chat.router)
