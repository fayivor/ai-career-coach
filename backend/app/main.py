from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chatbot, resume, skills, recommend, tracker
from app.services.ai_models import ai_models
from app.models.database import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Career Coach API",
    description="AI-powered career coaching platform with resume analysis, skill gap identification, and course recommendations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Load AI models and initialize database on startup"""
    logger.info("Starting AI Career Coach API...")

    # Initialize database
    logger.info("Initializing database...")
    init_db()

    # Load AI models
    await ai_models.load_models()

    logger.info("AI Career Coach API is ready!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Career Coach API",
        "version": "1.0.0",
        "endpoints": {
            "/api/chatbot": "Chat with AI career coach",
            "/api/resume": "Upload and analyze resume",
            "/api/skills": "Skill gap analysis",
            "/api/recommendations": "Get course recommendations",
            "/api/tracker": "Track career goals",
            "/docs": "Interactive API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": {
            "chatbot": ai_models.chatbot_model is not None,
            "summarizer": ai_models.summarizer is not None,
            "ner": ai_models.ner_model is not None,
            "sentence_transformer": ai_models.sentence_transformer is not None
        }
    }


# Include routers
app.include_router(chatbot.router)
app.include_router(resume.router)
app.include_router(skills.router)
app.include_router(recommend.router)
app.include_router(tracker.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
