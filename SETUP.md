# Setup & Installation Guide

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Package manager
- **OpenAI Account**: For API access

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Memory**: 2GB minimum
- **Storage**: 500MB for dependencies
- **Internet**: Required for API calls

## Step-by-Step Installation

### 1. Clone Repository

```bash
# Using git
git clone https://github.com/harish1817v/resume_screening.git
cd resume_screening

# Or download ZIP and extract
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Benefits of virtual environment:**
- Isolates project dependencies
- Prevents version conflicts
- Clean uninstall possible

### 3. Install Dependencies

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Dependencies installed:**
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation
- `PyPDF2` - PDF parsing
- `python-docx` - Word document parsing
- `langchain` - LLM framework support

### 4. Setup API Key

#### Get OpenAI API Key

1. Visit https://platform.openai.com/account/api-keys
2. Sign in with your OpenAI account (create one if needed)
3. Click "Create new secret key"
4. Copy the key immediately (won't show again)

#### Configure Environment

**Method 1: Create .env file (Recommended)**

```bash
# Copy example file
cp .env.example .env

# Edit .env with your editor
nano .env  # Linux/macOS
# or
notepad .env  # Windows
```

**File content:**
```env
OPENAI_API_KEY=sk-your-actual-key-here-xxx
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
LOG_LEVEL=INFO
```

**Method 2: Command-line (One-time)**

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Method 3: System Environment Variables**

Windows:
```bash
set OPENAI_API_KEY=sk-your-key-here
```

### 5. Verify Installation

```bash
# Test imports
python -c "import openai; import pydantic; print('✅ Core packages OK')"

# Try running demo
python main.py
```

Expected output:
```
✅ Configuration loaded successfully
   Using model: gpt-4

========================================
RESUME SCREENING SYSTEM
========================================
📋 Screening candidate...
```

## Troubleshooting

### Python Not Found

```
Error: Python command not recognized
```

**Solutions:**
- Windows: Add Python to PATH
- macOS/Linux: Use `python3` instead of `python`
- Install Python from https://www.python.org

### Module Not Found

```
ModuleNotFoundError: No module named 'openai'
```

**Solutions:**
```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### API Key Issues

```
Error: OpenAI API key is not configured
```

**Solutions:**
```bash
# Verify .env file exists
ls .env  # or: dir .env on Windows

# Check API key
grep OPENAI_API_KEY .env

# Test API connection
python -c "from src.config import settings; print(settings.is_configured)"
```

### PDF Parsing Error

```
Error: Failed to read PDF file
```

**Solutions:**
```bash
# Reinstall PyPDF2
pip install --force-reinstall PyPDF2

# Try with a different PDF
# Some PDFs have copy protection
```

### DOCX parsing error

```
Error: python-docx is required for DOCX support
```

**Solution:**
```bash
pip install python-docx
```

## Configuration Reference

### Model Selection

**GPT-4** (Recommended for accuracy)
- Most capable model
- Better understanding of complex resumes
- Slower (typical: 10-30 seconds per resume)
- More expensive ($0.03/$0.06 per 1K tokens)

**GPT-3.5-Turbo** (For speed)
- Faster processing
- Lower cost ($0.0005/$0.0015 per 1K tokens)
- Still accurate for most cases
- Typical: 3-10 seconds per resume

### Temperature Settings

```env
LLM_TEMPERATURE=0.0    # Deterministic (same output always)
LLM_TEMPERATURE=0.5    # Balanced (default)
LLM_TEMPERATURE=1.0    # Creative (more variation)
```

Lower temperature = more consistent
Higher temperature = more varied responses

### Token Limits

```env
LLM_MAX_TOKENS=1000    # Quick, economical
LLM_MAX_TOKENS=2000    # Balanced (default)
LLM_MAX_TOKENS=4000    # Very detailed
```

Higher = more detailed but slower and more expensive

## Development Setup

### Install Development Tools

```bash
# Testing framework
pip install pytest pytest-cov

# Code quality
pip install black flake8 mypy

# For local development, keep dependencies minimal
pip freeze > requirements-dev.txt
```

### IDE Configuration

**VS Code:**
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pythonPath": "${workspaceFolder}/venv/bin/python"
}
```

**PyCharm:**
1. Open Settings → Project → Python Interpreter
2. Click gear → Add
3. Select "Existing Environment"
4. Browse to `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)

## Usage After Installation

### Quick Test

```bash
# Run the demo
python main.py

# Output shows scoring report
```

### Process Your Files

```bash
from src.screening_engine import ScreeningEngine

engine = ScreeningEngine()

# Screen one resume
report = engine.screen_candidate(
    "path/to/resume.pdf",
    "job description text..."
)

# Print report
print(engine.generate_report_text(report))
```

### Batch Process

```bash
from examples.example_usage import batch_screen_candidates

batch_screen_candidates(
    "path/to/resumes/",
    "path/to/job_description.txt"
)
```

## Upgrade Guide

### Update Dependencies

```bash
# Show outdated packages
pip list --outdated

# Upgrade specific package
pip install --upgrade openai

# Upgrade all packages
pip install --upgrade -r requirements.txt
```

### Save New Dependencies

```bash
# After installing new package
pip freeze > requirements.txt
```

## Uninstall

```bash
# Remove virtual environment
rmvirtualenv resume_screening  # If using virtualenvwrapper

# Or manually
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Remove cloned directory
rm -rf resume_screening
```

## Performance Optimization

### Faster Installation

```bash
# Skip dependency resolution
pip install --no-deps -r requirements.txt

# Use binary packages only
pip install --only-binary :all: -r requirements.txt
```

### Reduce API Costs

1. Use GPT-3.5-turbo model
2. Reduce `LLM_MAX_TOKENS` to 1500
3. Cache job descriptions
4. Batch process resumes

### Faster Screening

1. Use GPT-3.5-turbo ($0 vs $0.03)
2. Reduce token limit
3. Run in parallel (if budget allows)

## Network Considerations

### Proxy Configuration

```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.company.com:8080'

from openai import OpenAI
```

### Offline Mode

Not currently supported (API calls required)

## Security Hardening

### For Production

1. **Rotate API Keys Regularly**
   ```bash
   # Update .env with new key
   ```

2. **Use IAM/Service Accounts**
   - Don't use personal API keys
   - Create dedicated service account

3. **Monitor Usage**
   - Check OpenAI dashboard regularly
   - Set billing alerts
   - Track API calls

4. **Secure Configuration**
   ```bash
   # Set strict permissions
   chmod 600 .env
   ```

---

## Next Steps

1. ✅ Complete installation
2. 📖 Read [README.md](README.md) for usage
3. 🏗️ Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
4. 👥 Check [examples/](examples/) for code samples
5. 🚀 Deploy to production

## Support

- 📧 Email: [support email]
- 🐛 Report bugs: [GitHub issues]
- 💬 Discussions: [GitHub discussions]
- 📚 Documentation: Full docs in code comments

---

**Last Updated:** 2024
**Version:** 1.0.0
