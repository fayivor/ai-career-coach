from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import CourseRecommendation
from app.services.course_recommender import course_recommender
from typing import List

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.post("/courses", response_model=CourseRecommendation)
async def recommend_courses(missing_skills: List[str], limit: int = Query(default=5, ge=1, le=20)):
    """
    Get course recommendations based on missing skills

    Args:
        missing_skills: List of skills to learn
        limit: Maximum number of courses to return (1-20)

    Returns:
        Recommended courses
    """
    try:
        if not missing_skills:
            raise HTTPException(status_code=400, detail="missing_skills cannot be empty")

        courses = course_recommender.recommend_courses(missing_skills, limit)

        return CourseRecommendation(
            courses=courses,
            total=len(courses)
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Course recommendation error: {str(e)}")


@router.get("/courses/all")
async def get_all_courses():
    """Get all available courses"""
    return {
        "courses": course_recommender.COURSES_DB,
        "total": len(course_recommender.COURSES_DB)
    }


@router.get("/courses/provider/{provider}")
async def get_courses_by_provider(provider: str):
    """Get courses from a specific provider"""
    provider_lower = provider.lower()
    courses = [
        course for course in course_recommender.COURSES_DB
        if course.provider.lower() == provider_lower
    ]

    if not courses:
        raise HTTPException(status_code=404, detail=f"No courses found for provider: {provider}")

    return {
        "provider": provider,
        "courses": courses,
        "total": len(courses)
    }


@router.get("/courses/level/{level}")
async def get_courses_by_level(level: str):
    """Get courses by difficulty level"""
    level_lower = level.lower()
    valid_levels = ["beginner", "intermediate", "advanced"]

    if level_lower not in valid_levels:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid level. Must be one of: {', '.join(valid_levels)}"
        )

    courses = [
        course for course in course_recommender.COURSES_DB
        if course.level.lower() == level_lower
    ]

    return {
        "level": level,
        "courses": courses,
        "total": len(courses)
    }
