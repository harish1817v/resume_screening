"""
Demo script showing how to use the resume screening system.

This script demonstrates:
1. Single resume screening
2. Batch processing
3. Report generation and saving
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.screening_engine import ScreeningEngine
from src.config import settings


def demo_single_screening():
    """
    Demonstrate single resume screening.
    Uses the sample resume and job description included in examples folder.
    """
    print("=" * 80)
    print("DEMO: Single Resume Screening")
    print("=" * 80)
    print()
    
    # Load examples
    examples_dir = Path(__file__).parent
    resume_path = examples_dir / "sample_resume.txt"
    job_desc_path = examples_dir / "sample_job_description.txt"
    
    # Verify files exist
    if not resume_path.exists():
        print(f"❌ Resume file not found: {resume_path}")
        return
    
    if not job_desc_path.exists():
        print(f"❌ Job description file not found: {job_desc_path}")
        return
    
    # Read job description
    with open(job_desc_path, 'r') as f:
        job_description = f.read()
    
    # Initialize engine
    print("📋 Initializing screening engine...")
    engine = ScreeningEngine()
    print("✅ Engine initialized\n")
    
    # Screen the candidate
    print(f"📋 Screening resume: {resume_path.name}")
    print("   Processing with LLM (this may take 30-60 seconds)...\n")
    
    try:
        report = engine.screen_candidate(str(resume_path), job_description)
        print("✅ Screening complete!\n")
        
        # Display the text report
        print(engine.generate_report_text(report))
        
        # Save reports
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        json_path = output_dir / "demo_report.json"
        text_path = output_dir / "demo_report.txt"
        
        with open(json_path, 'w') as f:
            f.write(engine.generate_report_json(report))
        
        with open(text_path, 'w') as f:
            f.write(engine.generate_report_text(report))
        
        print()
        print("=" * 80)
        print("✅ Reports saved:")
        print(f"   JSON: {json_path}")
        print(f"   Text: {text_path}")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error during screening: {str(e)}")
        import traceback
        traceback.print_exc()


def demo_from_text():
    """
    Demonstrate screening with direct text input (no file parsing needed).
    """
    print("\n" + "=" * 80)
    print("DEMO: Direct Text Input (No File Parsing)")
    print("=" * 80)
    print()
    
    # Sample resume text
    resume_text = """
    Jane Smith
    jane.smith@email.com | (555) 987-6543
    
    Software Engineer with 6 years of experience
    
    TECHNICAL SKILLS:
    - Python, JavaScript, React
    - PostgreSQL, MongoDB
    - AWS, Docker
    
    EXPERIENCE:
    - Software Engineer at WebCorp (2020-Present)
      * Developed React applications
      * Worked on REST APIs in Python
      * Deployed applications to AWS
    
    - Junior Developer at StartUp (2018-2020)
      * Built web applications
      * Fixed bugs and improved performance
    
    EDUCATION:
    - B.S. Computer Science
    """
    
    # Sample job description
    job_description = """
    Senior Full Stack Engineer
    
    REQUIREMENTS:
    - 5+ years experience
    - Python backend development
    - React frontend experience
    - AWS knowledge
    - Microservices architecture
    
    DESIRED:
    - Kubernetes
    - CI/CD experience
    - Machine Learning basics
    """
    
    print("📋 Using text inputs directly (no file parsing)")
    print()
    
    try:
        from src.llm_integration import LLMAnalyzer
        from src.models import CandidateProfile, JobRequirements, ScreeningReport
        from datetime import datetime
        
        engine = ScreeningEngine()
        analyzer = LLMAnalyzer()
        
        # Analyze resume
        print("📄 Analyzing resume text...")
        resume_analysis = analyzer.analyze_resume(resume_text)
        candidate = CandidateProfile(raw_text=resume_text, **resume_analysis)
        print(f"   ✓ Extraction complete: {candidate.name or 'Candidate'}")
        
        # Analyze job
        print("📋 Analyzing job description...")
        job_analysis = analyzer.analyze_job_description(job_description)
        job = JobRequirements(raw_text=job_description, **job_analysis)
        print(f"   ✓ Extraction complete: {job.job_title or 'Position'}")
        
        # Evaluate
        print("🔍 Evaluating fit...")
        evaluation = analyzer.evaluate_fit(candidate, job)
        screening_result = engine._build_screening_result(evaluation)
        print(f"   ✓ Score: {screening_result.overall_score}/100")
        
        # Create report
        report = ScreeningReport(
            candidate_profile=candidate,
            job_requirements=job,
            screening_result=screening_result,
            timestamp=datetime.now().isoformat()
        )
        
        print()
        print(engine.generate_report_text(report))
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main demo entry point."""
    
    # Load environment
    load_dotenv()
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 18 + "RESUME SCREENING SYSTEM - DEMO" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Check configuration
    if not settings.is_configured:
        print("❌ ERROR: System not configured!")
        print()
        print("Please follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to .env")
        print("3. Save the file and run this script again")
        print()
        sys.exit(1)
    
    print(f"✅ System configured with model: {settings.llm_model}")
    print()
    
    # Run demos
    try:
        # Demo 1: Single file-based screening
        demo_single_screening()
        
        # Demo 2: Direct text input
        demo_from_text()
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
