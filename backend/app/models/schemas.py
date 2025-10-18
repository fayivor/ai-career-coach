from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    timestamp: str


class ResumeAnalysis(BaseModel):
    summary: str
    skills: List[str]
    experience: List[str]
    education: List[str]
    entities: dict


class SkillGapRequest(BaseModel):
    current_skills: List[str]
    target_role: str


class SkillGapResponse(BaseModel):
    missing_skills: List[str]
    matched_skills: List[str]
    gap_percentage: float
    recommendations: List[str]


class Course(BaseModel):
    title: str
    provider: str
    url: str
    duration: str
    level: str
    skills_covered: List[str]


class CourseRecommendation(BaseModel):
    courses: List[Course]
    total: int


class Goal(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    target_date: str
    status: str = "pending"
    created_at: Optional[str] = None


class GoalCreate(BaseModel):
    title: str
    description: str
    target_date: str


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[str] = None
    status: Optional[str] = None
