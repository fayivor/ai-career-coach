from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse
from app.services.career_knowledge import career_kb
from datetime import datetime

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat with the AI career coach (Smart Response System)

    Args:
        message: User's message

    Returns:
        Expert career coaching response (INSTANT)
    """
    try:
        if not message.message or len(message.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Use smart knowledge base for instant responses
        response_text = career_kb.get_response(message.message)

        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if chatbot model is loaded"""
    return {
        "status": "healthy",
        "model_loaded": ai_models.chatbot_model is not None
    }
