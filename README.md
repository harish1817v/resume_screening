# AI-Powered Resume Screening System

An intelligent resume screening system that leverages Large Language Models (LLMs) to automate candidate evaluation against job requirements. Built on the case study presented, this system provides context-aware matching, automated scoring, and data-driven hiring insights.

## 🎯 Overview

This system addresses key recruitment challenges by automating initial resume screening with AI, providing:

- **Context-Aware Matching**: Goes beyond keyword matching using semantic understanding
- **Automated Scoring**: Objective candidate evaluation (0-100 scale)
- **Profile Summarization**: Concise candidate insights for quick review
- **Gap Detection**: Identifies missing skills and experience
- **Risk Indicators**: Flags potential concerns for hiring teams
- **Explainability**: Transparent scoring with clear reasoning

## 🏗️ Project Structure

```
resume_screening/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management
│   ├── models.py                # Data models (Pydantic)
│   ├── resume_parser.py         # Resume file parsing (PDF, TXT, DOCX)
│   ├── llm_integration.py       # OpenAI API integration
│   └── screening_engine.py      # Core screening logic
├── examples/
│   ├── __init__.py
│   └── example_usage.py         # Usage examples
├── main.py                      # Entry point with demo
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
├── .gitignore                   # Git ignore rules
├── ARCHITECTURE.md              # Technical architecture details
├── SETUP.md                     # Installation & setup guide
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- OpenAI API key (get from https://platform.openai.com/account/api-keys)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/harish1817v/resume_screening.git
cd resume_screening

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# .env contents:
# OPENAI_API_KEY=sk-...your-key...
# LLM_MODEL=gpt-4
# LLM_TEMPERATURE=0.7
```

**⚠️ CRITICAL: API Key Security**
- Never commit `.env` to version control
- Keep your API key confidential
- `.env` is already in `.gitignore`
- Use `.env.example` as a template

### 4. Run the Demo

```bash
python main.py
```

Expected output:
```
✅ Configuration loaded successfully
   Using model: gpt-4

RESUME SCREENING SYSTEM
📋 Screening candidate...
✅ Reports saved
```

## 📋 Usage Guide

### Single Resume Screening

```python
from src.screening_engine import ScreeningEngine

# Initialize engine
engine = ScreeningEngine()

# Screen a candidate
report = engine.screen_candidate(
    resume_path="path/to/resume.pdf",
    job_description="Full job description text..."
)

# Generate reports
json_report = engine.generate_report_json(report)
text_report = engine.generate_report_text(report)

# Save reports
with open("report.json", "w") as f:
    f.write(json_report)
    
print(text_report)
```

### Batch Screening

```python
from examples.example_usage import batch_screen_candidates

# Screen all resumes in a directory
batch_screen_candidates(
    resumes_dir="path/to/resumes/",
    job_description_path="path/to/job_description.txt"
)
```

## 📊 Report Structure

### Output Fields

**Overall Score**: 0-100 rating
**Match Level**: Excellent (80-100), Good (60-79), Moderate (40-59), Poor (0-39)

**Strengths**: Relevant skills, experience, and achievements
- Relevance score for each strength
- Detailed explanation

**Gaps**: Missing skills, experience, or knowledge
- Importance level (High/Medium/Low)
- Impact description

**Risk Indicators**: Potential concerns
- Employment gaps
- Skill mismatches
- Inconsistencies

**Recommendations**: Actionable hiring guidance
- Interview focus areas
- Additional screening suggestions
- Onboarding considerations

### Example Report Output

```
================================================================================
RESUME SCREENING REPORT
================================================================================

CANDIDATE INFORMATION
----------------------------------------
Name: John Doe
Email: john.doe@email.com
Years of Experience: 8

SCREENING RESULTS
----------------------------------------
Overall Score: 82/100
Match Level: Excellent
Summary: Strong candidate with excellent technical skills and directly 
         relevant experience...

STRENGTHS
----------------------------------------
• Senior-level experience in full-stack development (Relevance: 95/100)
  8+ years with modern tech stack
• Container orchestration expertise (Relevance: 90/100)
  Kubernetes and Docker experience aligns perfectly
  
GAPS & MISSING COMPETENCIES
----------------------------------------
• Advanced Machine Learning (Importance: Low)
  Role requires ML, candidate has basic TensorFlow knowledge

RECOMMENDATIONS
----------------------------------------
1. Strong technical fit - proceed to technical interview
2. Focus interview on ML experience expansion
3. Consider for senior/lead role
```

## 🔧 Configuration Options

Edit `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...              # Your API key (required)
LLM_MODEL=gpt-4                    # Model: gpt-4, gpt-3.5-turbo
LLM_TEMPERATURE=0.7                # Randomness: 0 (deterministic) to 1 (creative)
LLM_MAX_TOKENS=2000                # Response length limit

# System Configuration
LOG_LEVEL=INFO                     # Logging: DEBUG, INFO, WARNING, ERROR
```

## 📁 Supported Resume Formats

- **PDF** (.pdf) - Most common format
- **Plain Text** (.txt) - Simple text files
- **Word Documents** (.docx) - Microsoft Word files

## 🔐 Security Best Practices

1. **API Key Management**
   ```python
   # ✅ GOOD - Load from environment
   from src.config import settings
   api_key = settings.openai_api_key
   ```

2. **Never hardcode credentials**
   ```python
   # ❌ BAD - Don't do this
   api_key = "sk-xyz123"
   ```

3. **Use .gitignore for sensitive files**
   - `.env` file is ignored
   - `.env.local` won't be committed
   - Credentials won't leak

## 🧪 Testing

```bash
# Run tests (if test suite exists)
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_resume_parser.py
```

## 🏆 Features & Implementation

### 1. **Resume Parsing** (`src/resume_parser.py`)
- Extracts text from multiple formats
- Handles various document structures
- Robust error handling

### 2. **LLM Integration** (`src/llm_integration.py`)
- OpenAI API integration
- Structured JSON responses
- Error handling and retry logic

### 3. **Screening Engine** (`src/screening_engine.py`)
- Orchestrates entire workflow
- Generates formatted reports
- Data validation and transformation

### 4. **Data Models** (`src/models.py`)
- Type-safe with Pydantic V2
- Clear structure for all entities
- Built-in validation

## 📈 Workflow Steps

```
résumé → Parse Text → Analyze with LLM → Extract Profile
                                              ↓
                                    Job Description → Parse → Analyze with LLM
                                              ↓
                                    Evaluate Fit with LLM
                                              ↓
                                    Generate Report
```

## 🐛 Troubleshooting

### API Key Error
```
Error: OpenAI API key is not configured
```
**Solution**: Set `OPENAI_API_KEY` in `.env` file

### File Format Error
```
ValueError: Unsupported file format: .docx
```
**Solution**: Ensure `python-docx` is installed: `pip install python-docx`

### JSON Parsing Error
```
ValueError: LLM response was not valid JSON
```
**Solution**: This is rare but can happen with very large documents. Try:
- Increasing `LLM_MAX_TOKENS` in `.env`
- Using GPT-4 for better reliability
- Checking resume formatting

## 💡 Quick Tips

### For Speed (Quick Screening)
```env
LLM_MODEL=gpt-3.5-turbo
LLM_MAX_TOKENS=1500
```

### For Accuracy (Detailed Analysis)
```env
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0
LLM_MAX_TOKENS=2500
```

## 📚 Documentation

- [Setup & Installation Guide](SETUP.md) - Detailed setup instructions
- [Architecture & Design](ARCHITECTURE.md) - Technical architecture
- [Example Usage](examples/example_usage.py) - Code examples

## 🚧 Future Enhancements

- [ ] Web UI for easier resume uploads
- [ ] Integration with ATS platforms (Lever, Greenhouse, etc.)
- [ ] Batch processing with queue management
- [ ] Custom evaluation criteria per role
- [ ] Resume comparison and ranking
- [ ] Interview scheduling automation
- [ ] Diversity & inclusion metrics
- [ ] Historical performance tracking
- [ ] API endpoint for integration

## 📝 API Reference

### Core Classes  

**ScreeningEngine**
- `screen_candidate(resume_path, job_description)`: Main analysis function
- `generate_report_json(report)`: Export as JSON
- `generate_report_text(report)`: Export as human-readable text

**ResumeParser**
- `extract_text(file_path)`: Extract text from any supported format
- `parse_resume(file_path)`: Create CandidateProfile

**LLMAnalyzer**
- `analyze_resume(resume_text)`: Extract resume data
- `analyze_job_description(job_text)`: Extract job requirements
- `evaluate_fit(candidate, job)`: Evaluate match

## 📄 Case Study Reference

This system is built on comprehensive analysis covering:

1. **Introduction** - Recruitment challenges and benefits of automation
2. **Problem Statement** - Manual screening limitations
3. **Objective** - Automated, consistent, data-driven evaluation
4. **Proposed Solution** - LLM-based intelligent matching
5. **Key Features** - Context-aware, automated, transparent
6. **Expected Benefits** - Speed, consistency, accuracy
7. **Implementation** - Phased development approach

## 🔗 References

- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python-docx](https://python-docx.readthedocs.io/)

## 📧 Support & Questions

- 🐛 Report bugs via GitHub issues
- 📖 Check documentation first
- 💬 Open discussions for questions

## 📄 License

[Add appropriate license here]

## 👤 Author

Harish Kumar V  
GitHub: [@harish1817v](https://github.com/harish1817v)

---

**Important Notes:**

1. **Cost Awareness**: This system uses OpenAI API, which incurs charges. Monitor your usage.
2. **API Rate Limits**: OpenAI has rate limits. Plan batch processing accordingly.
3. **Privacy**: Ensure compliance with data privacy regulations when processing resumes.
4. **Testing**: Always test with non-sensitive data first.

For complete setup instructions, see [SETUP.md](SETUP.md).  
For technical details, see [ARCHITECTURE.md](ARCHITECTURE.md).
