"""Core resume screening engine."""

import json
import logging
from datetime import datetime
from typing import Tuple
from .models import (
    CandidateProfile, JobRequirements, ScreeningResult,
    ScreeningReport, MatchLevel, Strength, Gap
)
from .resume_parser import ResumeParser
from .llm_integration import LLMAnalyzer

logger = logging.getLogger(__name__)


class ScreeningEngine:
    """Main engine for resume screening workflow."""
    
    def __init__(self):
        """Initialize the screening engine."""
        self.parser = ResumeParser()
        self.analyzer = LLMAnalyzer()
    
    def screen_candidate(
        self,
        resume_path: str,
        job_description: str
    ) -> ScreeningReport:
        """
        Perform complete screening of a candidate.
        
        Args:
            resume_path: Path to resume file
            job_description: Job description text
            
        Returns:
            Complete screening report
        """
        logger.info(f"Starting screening for resume: {resume_path}")
        
        # Step 1: Extract resume text
        resume_text = self.parser.extract_text(resume_path)
        logger.info("Resume text extracted")
        
        # Step 2: Analyze resume
        logger.info("Analyzing resume with LLM...")
        resume_analysis = self.analyzer.analyze_resume(resume_text)
        candidate_profile = self._build_candidate_profile(resume_text, resume_analysis)
        logger.info(f"Candidate profile extracted: {candidate_profile.name or 'Unknown'}")
        
        # Step 3: Analyze job description
        logger.info("Analyzing job description with LLM...")
        job_analysis = self.analyzer.analyze_job_description(job_description)
        job_requirements = self._build_job_requirements(job_description, job_analysis)
        logger.info(f"Job requirements extracted: {job_requirements.job_title or 'Unknown'}")
        
        # Step 4: Evaluate fit
        logger.info("Evaluating candidate fit...")
        evaluation = self.analyzer.evaluate_fit(candidate_profile, job_requirements)
        screening_result = self._build_screening_result(evaluation)
        logger.info(f"Screening complete. Score: {screening_result.overall_score}/100")
        
        # Step 5: Create report
        report = ScreeningReport(
            candidate_profile=candidate_profile,
            job_requirements=job_requirements,
            screening_result=screening_result,
            timestamp=datetime.now().isoformat()
        )
        
        return report
    
    def _build_candidate_profile(
        self,
        resume_text: str,
        analysis: dict
    ) -> CandidateProfile:
        """Build CandidateProfile from analysis."""
        return CandidateProfile(
            name=analysis.get('name'),
            email=analysis.get('email'),
            phone=analysis.get('phone'),
            years_of_experience=analysis.get('years_of_experience'),
            technical_skills=analysis.get('technical_skills', []),
            domain_expertise=analysis.get('domain_expertise', []),
            key_achievements=analysis.get('key_achievements', []),
            education=analysis.get('education', []),
            certifications=analysis.get('certifications', []),
            raw_text=resume_text
        )
    
    def _build_job_requirements(
        self,
        job_text: str,
        analysis: dict
    ) -> JobRequirements:
        """Build JobRequirements from analysis."""
        return JobRequirements(
            job_title=analysis.get('job_title'),
            required_skills=analysis.get('required_skills', []),
            desired_skills=analysis.get('desired_skills', []),
            years_of_experience_required=analysis.get('years_of_experience_required'),
            domain_expertise_required=analysis.get('domain_expertise_required', []),
            education_required=analysis.get('education_required', []),
            key_responsibilities=analysis.get('key_responsibilities', []),
            raw_text=job_text
        )
    
    def _build_screening_result(self, evaluation: dict) -> ScreeningResult:
        """Build ScreeningResult from evaluation."""
        match_level_str = evaluation.get('match_level', 'Poor')
        
        # Validate match level
        try:
            match_level = MatchLevel(match_level_str)
        except ValueError:
            match_level = MatchLevel.POOR
        
        # Build strengths
        strengths = [
            Strength(**strength) 
            for strength in evaluation.get('strengths', [])
        ]
        
        # Build gaps
        gaps = [
            Gap(**gap)
            for gap in evaluation.get('gaps', [])
        ]
        
        return ScreeningResult(
            overall_score=evaluation.get('overall_score', 0),
            match_level=match_level,
            summary=evaluation.get('summary', ''),
            strengths=strengths,
            gaps=gaps,
            risk_indicators=evaluation.get('risk_indicators', []),
            recommendations=evaluation.get('recommendations', []),
            detailed_analysis=evaluation
        )
    
    def generate_report_json(self, report: ScreeningReport) -> str:
        """
        Generate JSON report.
        
        Args:
            report: ScreeningReport object
            
        Returns:
            JSON string representation
        """
        return report.model_dump_json(indent=2)
    
    def generate_report_text(self, report: ScreeningReport) -> str:
        """
        Generate human-readable text report.
        
        Args:
            report: ScreeningReport object
            
        Returns:
            Formatted text report
        """
        output = []
        output.append("=" * 80)
        output.append("RESUME SCREENING REPORT")
        output.append("=" * 80)
        output.append("")
        
        # Candidate Information
        output.append("CANDIDATE INFORMATION")
        output.append("-" * 40)
        profile = report.candidate_profile
        output.append(f"Name: {profile.name or 'Not specified'}")
        output.append(f"Email: {profile.email or 'Not specified'}")
        output.append(f"Phone: {profile.phone or 'Not specified'}")
        output.append(f"Years of Experience: {profile.years_of_experience or 'Not specified'}")
        output.append("")
        
        # Job Information
        output.append("JOB INFORMATION")
        output.append("-" * 40)
        job = report.job_requirements
        output.append(f"Job Title: {job.job_title or 'Not specified'}")
        output.append(f"Experience Required: {job.years_of_experience_required or 'Not specified'} years")
        output.append("")
        
        # Screening Results
        result = report.screening_result
        output.append("SCREENING RESULTS")
        output.append("-" * 40)
        output.append(f"Overall Score: {result.overall_score}/100")
        output.append(f"Match Level: {result.match_level.value}")
        output.append(f"Summary: {result.summary}")
        output.append("")
        
        # Strengths
        output.append("STRENGTHS")
        output.append("-" * 40)
        if result.strengths:
            for strength in result.strengths:
                output.append(f"• {strength.strength} (Relevance: {strength.relevance_score}/100)")
                output.append(f"  {strength.description}")
        else:
            output.append("No significant strengths identified")
        output.append("")
        
        # Gaps
        output.append("GAPS & MISSING COMPETENCIES")
        output.append("-" * 40)
        if result.gaps:
            for gap in result.gaps:
                output.append(f"• {gap.skill_or_experience} (Importance: {gap.importance})")
                output.append(f"  {gap.description}")
        else:
            output.append("No significant gaps identified")
        output.append("")
        
        # Risk Indicators
        output.append("RISK INDICATORS")
        output.append("-" * 40)
        if result.risk_indicators:
            for risk in result.risk_indicators:
                output.append(f"• {risk}")
        else:
            output.append("No risk indicators identified")
        output.append("")
        
        # Recommendations
        output.append("RECOMMENDATIONS")
        output.append("-" * 40)
        if result.recommendations:
            for i, rec in enumerate(result.recommendations, 1):
                output.append(f"{i}. {rec}")
        else:
            output.append("No specific recommendations")
        output.append("")
        
        # Metadata
        output.append("REPORT METADATA")
        output.append("-" * 40)
        output.append(f"Generated: {report.timestamp}")
        output.append("=" * 80)
        
        return "\n".join(output)
