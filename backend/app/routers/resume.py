from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import ResumeAnalysis
from app.services.resume_processor import resume_processor
from app.services.ai_models import ai_models

router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.post("/analyze", response_model=ResumeAnalysis)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze uploaded resume (PDF or DOCX)

    Args:
        file: Resume file (PDF or DOCX)

    Returns:
        Resume analysis with summary, skills, experience, and entities
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx')):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported"
            )

        # Read file content
        content = await file.read()

        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            text = resume_processor.extract_text_from_pdf(content)
        else:
            text = resume_processor.extract_text_from_docx(content)

        if not text or len(text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from resume"
            )

        # Generate summary using AI
        summary = ai_models.summarize_text(text)

        # Extract skills
        skills = resume_processor.extract_skills(text)

        # Extract experience
        experience = resume_processor.extract_experience(text)

        # Extract education
        education = resume_processor.extract_education(text)

        # Extract entities (names, organizations, etc.)
        entities = ai_models.extract_entities(text[:1000])  # Limit text for NER

        return ResumeAnalysis(
            summary=summary,
            skills=skills,
            experience=experience,
            education=education,
            entities=entities
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis error: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if resume analyzer is ready"""
    return {
        "status": "healthy",
        "models_loaded": ai_models.summarizer is not None and ai_models.ner_model is not None
    }
