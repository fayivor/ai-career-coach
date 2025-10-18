from fastapi import APIRouter, HTTPException
from app.models.schemas import SkillGapRequest, SkillGapResponse
from app.services.ai_models import ai_models
from typing import Dict, List

router = APIRouter(prefix="/api/skills", tags=["Skills"])

# Mock job role requirements database
JOB_REQUIREMENTS: Dict[str, List[str]] = {
    "software engineer": [
        "Python", "JavaScript", "Git", "SQL", "REST API",
        "Data Structures", "Algorithms", "Testing"
    ],
    "data scientist": [
        "Python", "Machine Learning", "Data Science", "SQL",
        "TensorFlow", "PyTorch", "Statistics", "Data Visualization"
    ],
    "frontend developer": [
        "JavaScript", "React", "HTML", "CSS", "TypeScript",
        "Redux", "Git", "REST API"
    ],
    "backend developer": [
        "Python", "Node.js", "SQL", "REST API", "Docker",
        "Git", "Databases", "Microservices"
    ],
    "fullstack developer": [
        "JavaScript", "Python", "React", "Node.js", "SQL",
        "REST API", "Git", "Docker", "HTML", "CSS"
    ],
    "devops engineer": [
        "Docker", "Kubernetes", "CI/CD", "AWS", "Linux",
        "Git", "Python", "Terraform"
    ],
    "ml engineer": [
        "Python", "Machine Learning", "TensorFlow", "PyTorch",
        "Docker", "SQL", "Git", "Cloud Computing"
    ]
}


@router.post("/gap-analysis", response_model=SkillGapResponse)
async def analyze_skill_gap(request: SkillGapRequest):
    """
    Analyze skill gap between current skills and target role

    Args:
        request: Current skills and target role

    Returns:
        Skill gap analysis with missing skills and recommendations
    """
    try:
        # Normalize target role
        target_role = request.target_role.lower().strip()

        # Get required skills for the role
        required_skills = JOB_REQUIREMENTS.get(target_role)

        if not required_skills:
            # If role not found, suggest available roles
            available_roles = list(JOB_REQUIREMENTS.keys())
            raise HTTPException(
                status_code=404,
                detail=f"Role '{request.target_role}' not found. Available roles: {', '.join(available_roles)}"
            )

        # Calculate skill similarity using AI
        skill_analysis = ai_models.calculate_skill_similarity(
            request.current_skills,
            required_skills
        )

        # Generate recommendations
        recommendations = []
        if skill_analysis['missing_skills']:
            recommendations.append(
                f"Focus on learning: {', '.join(skill_analysis['missing_skills'][:3])}"
            )
            recommendations.append(
                "Consider taking online courses to bridge the gap"
            )
            recommendations.append(
                "Build projects showcasing these new skills"
            )

        return SkillGapResponse(
            missing_skills=skill_analysis['missing_skills'],
            matched_skills=skill_analysis['matched_skills'],
            gap_percentage=skill_analysis['gap_percentage'],
            recommendations=recommendations
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill gap analysis error: {str(e)}")


@router.get("/roles")
async def get_available_roles():
    """Get list of available job roles"""
    return {
        "roles": list(JOB_REQUIREMENTS.keys()),
        "total": len(JOB_REQUIREMENTS)
    }


@router.get("/role/{role_name}")
async def get_role_requirements(role_name: str):
    """Get required skills for a specific role"""
    role = role_name.lower().strip()
    if role not in JOB_REQUIREMENTS:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "role": role_name,
        "required_skills": JOB_REQUIREMENTS[role]
    }
