from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse
from app.services.gpt_chatbot import get_gpt_chatbot
from datetime import datetime
import os

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required. Please set it in your .env file or environment.")


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat with the AI career coach using OpenAI GPT

    Args:
        message: User's message

    Returns:
        AI-powered career coaching response with conversation memory
    """
    try:
        if not message.message or len(message.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Get GPT chatbot instance
        chatbot = get_gpt_chatbot(api_key=OPENAI_API_KEY)

        # Get response from GPT with conversation history
        response_text = chatbot.chat(message.message, use_history=True)

        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/clear")
async def clear_history():
    """Clear conversation history"""
    try:
        chatbot = get_gpt_chatbot(api_key=OPENAI_API_KEY)
        chatbot.clear_history()
        return {"message": "Conversation history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if GPT chatbot is configured"""
    try:
        chatbot = get_gpt_chatbot(api_key=OPENAI_API_KEY)
        return {
            "status": "healthy",
            "model": "gpt-3.5-turbo",
            "conversation_length": chatbot.get_history_length()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
