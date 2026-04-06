# System Architecture & Implementation Details

## Overview

This document provides technical details about the AI-powered Resume Screening System architecture, design decisions, and implementation patterns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Resume Screening System                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────┐         ┌──────────────────────┐       │
│  │  User Interface    │         │   API Integration    │       │
│  │  - CLI / Web UI    │────────▶│   - Main Application │       │
│  └────────────────────┘         └──────────────────────┘       │
│                                          │                     │
│                                          ▼                     │
│                        ┌──────────────────────────────┐        │
│                        │  ScreeningEngine             │        │
│                        │  - Orchestrates workflow     │        │
│                        │  - Manages data flow         │        │
│                        └──────────────────────────────┘        │
│           ┌─────────────────────┼─────────────────────┐        │
│           ▼                     ▼                     ▼        │
│   ┌──────────────┐      ┌──────────────┐      ┌────────────┐  │
│   │Resume Parser │      │LLM Analyzer  │      │   Models   │  │
│   │- PDF/TXT/DOCX       │- OpenAI API  │      │- Pydantic  │  │
│   │- Text Extract       │- JSON Parse  │      │- Validation│  │
│   └──────────────┘      └──────────────┘      └────────────┘  │
│           │                     │                              │
│           └─────────────────────┼──────────────────────────┐   │
│                                 ▼                          ▼   │
│                        ┌─────────────────────────────────────┐ │
│                        │  Config Management                  │ │
│                        │  - Environment variables            │ │
│                        │  - API key management               │ │
│                        │  - Settings validation              │ │
│                        └─────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Configuration Management (`src/config.py`)

**Purpose**: Centralized configuration using environment variables

**Design Pattern**: Singleton with Pydantic

```python
class Settings(BaseSettings):
    openai_api_key: str                    # API Key (required)
    llm_model: str = "gpt-4"              # Model selection
    llm_temperature: float = 0.7          # Response randomness
    llm_max_tokens: int = 2000            # Response length
    log_level: str = "INFO"               # Logging level
```

**Benefits**:
- Type-safe configuration
- Automatic validation
- Environment-based (secure)
- Single source of truth

### 2. Data Models (`src/models.py`)

**Purpose**: Type-safe data structures with validation

**Using Pydantic V2** for:
- Runtime validation
- Clear API contracts
- Easy serialization (JSON)
- IDE autocompletion

**Key Models**:
- `CandidateProfile`: Parsed resume information
- `JobRequirements`: Parsed job description
- `ScreeningResult`: AI evaluation output
- `ScreeningReport`: Complete result package

### 3. Resume Parser (`src/resume_parser.py`)

**Purpose**: Extract text from various resume formats

**Supported Formats**:
- PDF (using PyPDF2)
- Plain Text (.txt)
- Word Documents (.docx)

**Design Pattern**: Strategy Pattern

```python
class ResumeParser:
    @staticmethod
    def extract_text(file_path: str) -> str
        # Route to appropriate parser based on file extension
    
    def _extract_from_pdf(file_path: str) -> str
    def _extract_from_txt(file_path: str) -> str
    def _extract_from_docx(file_path: str) -> str
```

**Error Handling**:
- Validates file format
- Graceful error messages
- Try-catch with logging

### 4. LLM Integration (`src/llm_integration.py`)

**Purpose**: Interface with OpenAI API for intelligent analysis

**Three Main Operations**:

#### a. Resume Analysis
```python
def analyze_resume(resume_text: str) -> Dict[str, Any]
```
Extracts structured information:
- Personal details (name, email, phone)
- Technical skills
- Domain expertise
- Achievements
- Education & certifications

#### b. Job Description Analysis
```python
def analyze_job_description(job_text: str) -> Dict[str, Any]
```
Extracts requirements:
- Job title
- Required skills
- Desired skills
- Experience needed
- Key responsibilities

#### c. Fit Evaluation
```python
def evaluate_fit(
    candidate_profile: CandidateProfile,
    job_requirements: JobRequirements
) -> Dict[str, Any]
```
Returns:
- Overall score (0-100)
- Match level classification
- Strengths with relevance scores
- Gaps and missing competencies
- Risk indicators
- Recommendations

**Prompt Engineering**:
- Structured output (JSON format specified)
- Clear field definitions
- Error handling for malformed responses
- Temperature tuned for consistency

### 5. Screening Engine (`src/screening_engine.py`)

**Purpose**: Orchestrate complete screening workflow

**Workflow**:
```
1. Parse resume file
2. Analyze resume with LLM
3. Analyze job description with LLM
4. Evaluate candidate fit
5. Build report objects
6. Generate formatted output
```

**Report Generation**:
- JSON format (structured data)
- Human-readable text (for viewing)
- Timestamp tracking
- Complete data preservation

## Data Flow

### Input Processing

```
Resume File (PDF/TXT/DOCX)
        ↓
    [Parser]
        ↓
Raw Text String
        ↓
    [LLM Analysis]
        ↓
JSON with Extracted Fields
        ↓
    [Pydantic Validation]
        ↓
CandidateProfile Object
```

### Evaluation Processing

```
CandidateProfile + JobRequirements
        ↓
    [LLM Evaluate Fit]
        ↓
JSON with Scores & Analysis
        ↓
    [Build ScreeningResult]
        ↓
ScreeningResult Object
        ↓
    [Create Report]
        ↓
ScreeningReport (JSON + Text)
```

## Key Design Decisions

### 1. Pydantic V2 for Models

**Why**: 
- Type safety with runtime validation
- Clear API contracts
- Automatic JSON serialization
- Better IDE support

### 2. Environment-Based Configuration

**Why**:
- Secure (no hardcoded credentials)
- Different settings per environment
- Easy CI/CD integration
- Follows 12-factor app principles

### 3. Separation of Concerns

- **Parser**: Handles file format complexity
- **LLM Integration**: Manages API calls
- **Engine**: Orchestrates workflow
- **Models**: Ensures data integrity

### 4. JSON-based LLM Responses

**Why**:
- Structured, parseable output
- Easy validation and transformation
- Language-agnostic
- Enables downstream automation

## Error Handling Strategy

```python
# 1. Input Validation
- File format checking
- Configuration validation
- API key presence

# 2. API Error Handling
- JSON parsing failures
- API rate limits
- Network issues

# 3. Business Logic Validation
- Data type checking (Pydantic)
- Score range validation
- Required field checking

# 4. Graceful Degradation
- Meaningful error messages
- Logging for debugging
- User-friendly exceptions
```

## Performance Considerations

### API Costs

```
LLM Model          | Cost per 1K tokens | Speed
gpt-4              | $0.03/$0.06        | Slower (more accurate)
gpt-3.5-turbo      | $0.0005/$0.0015    | Faster (less accurate)
```

### Optimization Tips

1. **Batch Processing**: Screen multiple resumes in parallel
2. **Model Selection**: Use gpt-3.5-turbo for speed, gpt-4 for accuracy
3. **Token Optimization**: Trim unnecessary text before sending
4. **Caching**: Cache job descriptions when screening multiple candidates

## Security Architecture

### API Key Protection

```python
# Environment-based loading
from dotenv import load_dotenv
load_dotenv()  # Loads from .env
api_key = os.getenv('OPENAI_API_KEY')  # Retrieved securely
```

### Best Practices Implemented

1. **No Hardcoded Credentials**
   - All keys in environment variables
   - .env excluded from version control

2. **Credential Validation**
   - System checks for key presence on startup
   - Clear error messages if missing

3. **Secure Defaults**
   - Example file uses placeholder
   - Documentation emphasizes credential security

## Extensibility

### Adding New Resume Formats

```python
# In resume_parser.py
@staticmethod
def _extract_from_odt(file_path: str) -> str:
    """Add OpenDocument support"""
    from odf import opendocument
    # Implementation here

# Register in SUPPORTED_FORMATS
SUPPORTED_FORMATS = {'.pdf', '.txt', '.docx', '.odt'}
```

### Adding Custom Evaluation Criteria

```python
# Modify prompts in llm_integration.py
def evaluate_fit(...) -> Dict[str, Any]:
    prompt = f"""Custom evaluation criteria for {job_title}:
    1. Technical fit (40% weight)
    2. Cultural fit (30% weight)
    3. Growth potential (30% weight)
    ..."""
```

### Integration with ATS

```python
# Create new module: src/ats_integration.py
def send_to_ats(report: ScreeningReport) -> bool:
    """Send screening results to Applicant Tracking System"""
    # API calls to Lever, Greenhouse, etc.
```

## Testing Strategy

### Unit Tests
- Parser functionality
- Model validation
- Configuration loading

### Integration Tests
- End-to-end screening workflow
- LLM API mocking
- Report generation

### Performance Tests
- API response times
- Memory usage with large batches
- Concurrent request handling

## Deployment Considerations

### Production Checklist

- [ ] Replace `.env` with actual credentials in deployment
- [ ] Set up monitoring/logging
- [ ] Configure API rate limits
- [ ] Set up error alerts
- [ ] Document rollback procedures
- [ ] Test with production data volume

### Containerization (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Scaling Considerations

- API rate limiting (429 responses)
- Queue system for batch processing
- Distributed processing with task workers
- Caching results for similar evaluations

---

**Last Updated**: 2024
**Version**: 1.0.0
