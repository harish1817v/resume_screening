"""Main entry point for the resume screening system."""

import logging
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from src.screening_engine import ScreeningEngine
from src.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level, "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Verify configuration
    if not settings.is_configured:
        logger.error("❌ OpenAI API key not configured!")
        print("\n⚠️  ERROR: OpenAI API key is not configured.")
        print("\nTo set up the system:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key from https://platform.openai.com/account/api-keys")
        print("3. Run the script again\n")
        sys.exit(1)
    
    print("✅ Configuration loaded successfully")
    print(f"   Using model: {settings.llm_model}\n")
    
    # Example usage
    print("=" * 80)
    print("RESUME SCREENING SYSTEM - AI Powered Candidate Evaluation")
    print("=" * 80)
    print()
    
    # Initialize screening engine
    engine = ScreeningEngine()
    
    # Example: screening a candidate
    # In real usage, these would come from user input or file system
    example_resume = """
    John Doe
    john.doe@email.com | (555) 123-4567
    
    Senior Software Engineer with 8 years of experience in full-stack web development.
    
    TECHNICAL SKILLS:
    - Python, JavaScript, TypeScript
    - React, Node.js, Django, FastAPI
    - PostgreSQL, MongoDB, Redis
    - Docker, Kubernetes, AWS
    - Machine Learning: TensorFlow, PyTorch
    
    EXPERIENCE:
    - Senior Software Engineer at Tech Corp (2020-Present)
      * Led team of 5 engineers in developing microservices architecture
      * Improved API response time by 40% through optimization
      * Implemented CI/CD pipeline reducing deployment time from 2 hours to 15 minutes
    
    - Full Stack Developer at StartUp Inc (2018-2020)
      * Built scalable e-commerce platform serving 100K+ users
      * Designed and implemented real-time notification system
    
    EDUCATION:
    - B.S. Computer Science, State University (2015)
    
    CERTIFICATIONS:
    - AWS Certified Solutions Architect
    - Kubernetes Application Developer
    """
    
    example_job_description = """
    Senior Full Stack Engineer
    
    We are looking for an experienced Full Stack Engineer to join our growing team.
    
    REQUIREMENTS:
    - 5+ years of professional software development experience
    - Strong proficiency in Python or Java
    - Experience with React or Vue.js for frontend development
    - Database design and optimization skills (SQL and NoSQL)
    - Experience with cloud platforms (AWS, GCP, or Azure)
    - Understanding of microservices architecture
    
    DESIRED SKILLS:
    - Experience with Kubernetes and Docker
    - Machine Learning knowledge
    - Business acumen and ability to translate requirements
    - AWS certifications
    
    RESPONSIBILITIES:
    - Design and develop scalable full-stack applications
    - Collaborate with product and design teams
    - Mentor junior engineers
    - Participate in code reviews and architecture discussions
    """
    
    try:
        print("📋 Screening candidate...")
        print()
        
        # Perform screening (using example data instead of files)
        # In production, you would pass actual file paths
        from src.llm_integration import LLMAnalyzer
        from src.models import CandidateProfile, JobRequirements
        
        analyzer = LLMAnalyzer()
        
        # Analyze resume
        resume_analysis = analyzer.analyze_resume(example_resume)
        candidate = CandidateProfile(
            raw_text=example_resume,
            **resume_analysis
        )
        
        # Analyze job description
        job_analysis = analyzer.analyze_job_description(example_job_description)
        job = JobRequirements(
            raw_text=example_job_description,
            **job_analysis
        )
        
        # Evaluate fit
        evaluation = analyzer.evaluate_fit(candidate, job)
        
        from src.screening_engine import ScreeningEngine as SE
        engine_instance = SE()
        screening_result = engine_instance._build_screening_result(evaluation)
        
        from src.models import ScreeningReport
        report = ScreeningReport(
            candidate_profile=candidate,
            job_requirements=job,
            screening_result=screening_result,
            timestamp=__import__('datetime').datetime.now().isoformat()
        )
        
        # Generate and display report
        print(engine_instance.generate_report_text(report))
        
        # Save JSON report
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        report_json_path = output_dir / "screening_report.json"
        with open(report_json_path, 'w') as f:
            f.write(engine_instance.generate_report_json(report))
        
        print(f"\n✅ Full JSON report saved to: {report_json_path}")
        
    except Exception as e:
        logger.error(f"Error during screening: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
