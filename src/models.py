"""Data models for resume screening system."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class MatchLevel(str, Enum):
    """Enum for match levels."""
    EXCELLENT = "Excellent"
    GOOD = "Good"
    MODERATE = "Moderate"
    POOR = "Poor"


class Gap(BaseModel):
    """Model for skill or experience gaps."""
    skill_or_experience: str
    importance: str  # High, Medium, Low
    description: str


class Strength(BaseModel):
    """Model for candidate strengths."""
    strength: str
    relevance_score: int = Field(ge=0, le=100)
    description: str


class CandidateProfile(BaseModel):
    """Model for extracted candidate profile."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    years_of_experience: Optional[int] = None
    technical_skills: List[str] = []
    domain_expertise: List[str] = []
    key_achievements: List[str] = []
    education: List[str] = []
    certifications: List[str] = []
    raw_text: str


class JobRequirements(BaseModel):
    """Model for job description requirements."""
    job_title: Optional[str] = None
    required_skills: List[str] = []
    desired_skills: List[str] = []
    years_of_experience_required: Optional[int] = None
    domain_expertise_required: List[str] = []
    education_required: List[str] = []
    key_responsibilities: List[str] = []
    raw_text: str


class ScreeningResult(BaseModel):
    """Model for complete screening result."""
    overall_score: int = Field(ge=0, le=100)
    match_level: MatchLevel
    summary: str
    strengths: List[Strength]
    gaps: List[Gap]
    risk_indicators: List[str]
    recommendations: List[str]
    detailed_analysis: Dict[str, Any]


class ScreeningReport(BaseModel):
    """Complete screening report."""
    candidate_profile: CandidateProfile
    job_requirements: JobRequirements
    screening_result: ScreeningResult
    timestamp: str
