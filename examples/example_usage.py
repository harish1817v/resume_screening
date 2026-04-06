"""Example usage of the resume screening system."""

import json
from pathlib import Path
from dotenv import load_dotenv
from src.screening_engine import ScreeningEngine

# Load environment variables
load_dotenv()


def screen_resume_from_files(resume_path: str, job_description_path: str):
    """
    Screen a resume against a job description using file paths.
    
    Args:
        resume_path: Path to resume file (PDF, TXT, or DOCX)
        job_description_path: Path to job description file
    """
    
    # Initialize screening engine
    engine = ScreeningEngine()
    
    # Read job description
    with open(job_description_path, 'r') as f:
        job_description = f.read()
    
    # Perform screening
    report = engine.screen_candidate(resume_path, job_description)
    
    # Save reports
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON report
    json_path = output_dir / "screening_report.json"
    with open(json_path, 'w') as f:
        f.write(engine.generate_report_json(report))
    
    # Save text report
    text_path = output_dir / "screening_report.txt"
    with open(text_path, 'w') as f:
        f.write(engine.generate_report_text(report))
    
    print(f"✅ Reports saved:")
    print(f"   - JSON: {json_path}")
    print(f"   - Text: {text_path}")
    print()
    print(engine.generate_report_text(report))


def batch_screen_candidates(resumes_dir: str, job_description_path: str):
    """
    Screen multiple resumes against a single job description.
    
    Args:
        resumes_dir: Directory containing resume files
        job_description_path: Path to job description file
    """
    
    engine = ScreeningEngine()
    
    # Read job description
    with open(job_description_path, 'r') as f:
        job_description = f.read()
    
    # Get all resume files
    resumes_path = Path(resumes_dir)
    resume_files = list(resumes_path.glob("**/*.pdf")) + \
                   list(resumes_path.glob("**/*.txt")) + \
                   list(resumes_path.glob("**/*.docx"))
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for resume_file in resume_files:
        print(f"Screening: {resume_file.name}...", end=" ")
        
        try:
            report = engine.screen_candidate(str(resume_file), job_description)
            results.append({
                "file": resume_file.name,
                "score": report.screening_result.overall_score,
                "match": report.screening_result.match_level.value,
                "candidate": report.candidate_profile.name or "Unknown"
            })
            print(f"✅ Score: {report.screening_result.overall_score}/100")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Save summary
    summary_path = output_dir / "batch_results.json"
    with open(summary_path, 'w') as f:
        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Batch results saved to: {summary_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("BATCH SCREENING SUMMARY")
    print("=" * 60)
    for result in results:
        print(f"{result['candidate']:<30} {result['score']:>3}/100  ({result['match']})")


if __name__ == "__main__":
    print("Resume Screening System - Example Usage")
    print("=" * 60)
    print()
    print("Available functions:")
    print("1. screen_resume_from_files(resume_path, job_description_path)")
    print("2. batch_screen_candidates(resumes_dir, job_description_path)")
    print()
    print("Example:")
    print("  from examples.example_usage import screen_resume_from_files")
    print("  screen_resume_from_files('path/to/resume.pdf', 'path/to/job.txt')")
