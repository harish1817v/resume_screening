# 🚀 Getting Started - 5 Minutes

A quick guide to get the resume screening system running in 5 minutes.

## Step 1: Clone & Enter Directory (30 seconds)

```bash
git clone https://github.com/harish1817v/resume_screening.git
cd resume_screening
```

## Step 2: Create Virtual Environment (30 seconds)

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

## Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 4: Setup API Key (2 minutes)

1. **Get your API key**: Go to https://platform.openai.com/account/api-keys
2. **Sign in** to OpenAI (create account if needed)
3. **Create new secret key** and copy it
4. **Create .env file**:

```bash
cp .env.example .env
```

5. **Add your key** (edit .env with your editor):

```env
OPENAI_API_KEY=sk-your-actual-key-here-xxx
```

## Step 5: Run the Demo (30 seconds)

```bash
python main.py
```

You should see a screening report!

## Current Files

```
✅ src/                    - Core system code
✅ examples/               - Demo and examples
✅ README.md               - Full documentation
✅ SETUP.md                - Detailed setup guide
✅ ARCHITECTURE.md         - Technical details
✅ requirements.txt        - Dependencies
✅ .env.example           - Config template
✅ .gitignore             - Git ignore rules
```

## Next Steps

### Try the Demo
```bash
python examples/demo.py
```

### Screen Your Own Resume
```python
from src.screening_engine import ScreeningEngine

engine = ScreeningEngine()
report = engine.screen_candidate(
    "your_resume.pdf",
    "job_description_text_here"
)
print(engine.generate_report_text(report))
```

### Batch Process Multiple Resumes
```python
from examples.example_usage import batch_screen_candidates

batch_screen_candidates(
    "path/to/resume/folder",
    "job_description.txt"
)
```

## Supported Resume Formats

- 📄 PDF files (.pdf)
- 📝 Text files (.txt)
- 📋 Word documents (.docx)

## What You Get

```
Resume Input
    ↓
PDF/TXT/DOCX Parsing
    ↓
LLM Analysis
    ↓
Smart Evaluation
    ↓
Output Report
├── Overall Score (0-100)
├── Match Level (Excellent/Good/Moderate/Poor)
├── Strengths
├── Gaps
├── Risk Indicators
└── Recommendations
```

## Important Notes

⚠️ **API Key Security**
- Keep your `.env` file private
- Never share your API key
- Never commit `.env` to git (already in .gitignore)

💰 **Costs**
- OpenAI charges per API call
- ~$0.005-0.05 per resume
- Monitor your usage at https://platform.openai.com/account/usage

## Troubleshooting

| Issue | Solution |
|---|---|
| Python not found | Install from https://www.python.org |
| API key error | Check your .env file has the correct key |
| Module not found | Run `pip install -r requirements.txt` |
| Permission denied (.env) | Make sure file is readable |

## Full Documentation

- 📖 **Complete setup**: [SETUP.md](SETUP.md)
- 🏗️ **Technical details**: [ARCHITECTURE.md](ARCHITECTURE.md)
- 📚 **Features & usage**: [README.md](README.md)
- 📋 **What was built**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## Quick Tips

🚀 **For testing:**
```bash
python main.py
```

⚡ **For faster screening:**
```env
LLM_MODEL=gpt-3.5-turbo
```

🎯 **For better accuracy:**
```env
LLM_MODEL=gpt-4
```

---

**Ready?** Start with `python main.py` !

Need help? Check [SETUP.md](SETUP.md) or [README.md](README.md).
