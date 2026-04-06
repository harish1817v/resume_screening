"""LLM integration module for AI-powered analysis."""

import json
import logging
from typing import Dict, Any
from openai import OpenAI
from .config import settings
from .models import CandidateProfile, JobRequirements, ScreeningResult, MatchLevel

logger = logging.getLogger(__name__)


class LLMAnalyzer:
    """Handles LLM-based analysis of resumes and job descriptions."""
    
    def __init__(self):
        """Initialize LLM client."""
        if not settings.is_configured:
            raise ValueError(
                "OpenAI API key is not configured. "
                "Please set OPENAI_API_KEY in .env file"
            )
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume text and extract structured information.
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Structured resume information
        """
        prompt = f"""Analyze the following resume and extract structured information.
Return a JSON object with the following fields:
- name: Candidate name (or null if not found)
- email: Email address (or null)
- phone: Phone number (or null)
- years_of_experience: Total years of experience (or null)
- technical_skills: List of technical skills
- domain_expertise: List of domain areas of expertise
- key_achievements: List of key achievements/accomplishments
- education: List of educational qualifications
- certifications: List of certifications and credentials

Resume:
{resume_text}

Return only valid JSON, no additional text."""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.choices[0].message.content.strip()
            return json.loads(result_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise ValueError("LLM response was not valid JSON")
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            raise
    
    def analyze_job_description(self, job_text: str) -> Dict[str, Any]:
        """
        Analyze job description and extract requirements.
        
        Args:
            job_text: Raw job description text
            
        Returns:
            Structured job requirements
        """
        prompt = f"""Analyze the following job description and extract requirements.
Return a JSON object with the following fields:
- job_title: Job title (or null if not found)
- required_skills: List of required technical skills
- desired_skills: List of desired/nice-to-have skills
- years_of_experience_required: Minimum years of experience required (or null)
- domain_expertise_required: List of required domain expertise areas
- education_required: List of required educational qualifications
- key_responsibilities: List of key job responsibilities

Job Description:
{job_text}

Return only valid JSON, no additional text."""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.choices[0].message.content.strip()
            return json.loads(result_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise ValueError("LLM response was not valid JSON")
        except Exception as e:
            logger.error(f"Error analyzing job description: {e}")
            raise
    
    def evaluate_fit(
        self,
        candidate_profile: CandidateProfile,
        job_requirements: JobRequirements
    ) -> Dict[str, Any]:
        """
        Evaluate how well candidate fits the job.
        
        Args:
            candidate_profile: Extracted candidate information
            job_requirements: Extracted job requirements
            
        Returns:
            Structured evaluation result
        """
        prompt = f"""You are an expert recruiter. Evaluate the fit between a candidate and a job position.

CANDIDATE PROFILE:
{candidate_profile.model_dump_json(indent=2)}

JOB REQUIREMENTS:
{job_requirements.model_dump_json(indent=2)}

Provide a detailed evaluation in JSON format with:
- overall_score: Integer score from 0-100
- match_level: One of "Excellent" (80-100), "Good" (60-79), "Moderate" (40-59), "Poor" (0-39)
- summary: Brief summary of overall fit
- strengths: Array of objects with {{strength: string, relevance_score: 0-100, description: string}}
- gaps: Array of objects with {{skill_or_experience: string, importance: "High/Medium/Low", description: string}}
- risk_indicators: List of potential concerns or red flags
- recommendations: List of recommendations for the hiring team

Ensure your response is valid JSON with no additional text."""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.choices[0].message.content.strip()
            return json.loads(result_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise ValueError("LLM response was not valid JSON")
        except Exception as e:
            logger.error(f"Error evaluating fit: {e}")
            raise
