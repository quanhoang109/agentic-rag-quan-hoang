# Lesson 1: Setup Instructions

## Step-by-Step Guide

### Part 1: Install uv Package Manager

**Why uv?** uv is a modern, fast Python package manager (10-100x faster than pip) developed by Astral. It simplifies dependency management and virtual environments.

```bash
# Install uv using pip
pip install uv

# Verify installation
uv --version
# Should show: uv 0.x.x
```

**Alternative installation methods:**
```bash
# macOS/Linux (recommended):
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell):
irm https://astral.sh/uv/install.ps1 | iex
```

### Part 2: Create Virtual Environment with uv

**Why?** Virtual environments isolate project dependencies from your system Python.

```bash
# Navigate to project root
cd /path/to/agentic-rag

# Create virtual environment using uv (much faster!)
uv venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# You should see (.venv) in your terminal prompt
```

**Note:** uv creates `.venv` by default (not `venv`). Both work fine!

### Part 3: Install Dependencies with uv

```bash
# Install all required packages using uv (10-100x faster than pip!)
uv pip install -r requirements.txt

# This will install:
# - openai-agents (multi-agent framework)
# - openai (API client)
# - chromadb (vector database)
# - flask & flask_cors (API server)
# - streamlit (UI framework)
# - pandas (data processing)
# - python-dotenv (environment variables)
# - and more...
```

**Why uv is faster:**
- Parallel downloads
- Optimized resolver
- Cached dependencies
- Native code (written in Rust)

**Verification:**
```bash
uv pip list | grep openai
# Should show: openai, openai-agents
```

**Alternative (using standard pip):**
If you prefer traditional pip:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Part 4: Set Up Environment Variables

**1. Create .env file:**
```bash
# Copy template
cp .env.example .env
```

**2. Edit .env file:**
```bash
# Open in your editor
nano .env  # or use VS Code, vim, etc.
```

**3. Add your API keys:**
```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Optional: OpenRouter for alternative models
OPENROUTER_API_KEY=sk-or-your-actual-key-here

# Optional: Google Sheets (for Lesson 7)
GOOGLE_SHEETS_CREDENTIALS_FILE=your-credentials.json
GOOGLE_SHEETS_URL=your-sheet-url
```

**Getting API Keys:**

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (you won't see it again!)
5. Paste into .env file

**OpenRouter (Optional):**
1. Go to https://openrouter.ai/keys
2. Sign in or create account
3. Click "Create Key"
4. Copy and paste into .env file

**⚠️ Security Notes:**
- NEVER commit .env to git
- Keep API keys private
- Regenerate if accidentally exposed
- The .env file is already in .gitignore

### Part 5: Verify Installation

Run the verification script:

```bash
python lessons/lesson-01-setup/solution/verify.py
```

**Expected output:**
```
✓ Python version: 3.10.x (OK)
✓ uv: Installed (uv 0.x.x)
✓ Virtual environment: Active
✓ OpenAI package: Installed (version 1.99.9)
✓ OpenAI Agents SDK: Installed (version 0.2.8)
✓ ChromaDB: Installed
✓ Flask: Installed
✓ Streamlit: Installed
✓ .env file: Found
✓ OPENAI_API_KEY: Set
✓ OpenAI API: Connection successful
✓ Embedding test: Passed

All checks passed! ✅
Your environment is ready for Lesson 2.
```

### Part 6: Test OpenAI Connection

Quick test to ensure API key works:

```python
# test_api.py
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test embedding generation
response = client.embeddings.create(
    input="Hello, world!",
    model="text-embedding-3-small"
)

print(f"✓ Embedding generated: {len(response.data[0].embedding)} dimensions")
```

Run it:
```bash
python test_api.py
```

Expected: `✓ Embedding generated: 1536 dimensions`

## Common Issues

### Issue 1: "uv: command not found"
**Solution:** Install uv package manager
```bash
pip install uv
# Or use curl (recommended):
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Issue 2: "Permission denied"
**Solution:** Use uv with virtual environment (automatically isolated)
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Issue 3: "ModuleNotFoundError: No module named 'dotenv'"
**Solution:** Virtual environment not activated
```bash
source .venv/bin/activate  # Activate first (uv creates .venv)
uv pip install python-dotenv
```

### Issue 4: "AuthenticationError: Invalid API key"
**Solution:** Check .env file
- No spaces around `=`
- No quotes around key
- Correct key from OpenAI dashboard

### Issue 5: ".env file not loading"
**Solution:** Check file location
```bash
# .env should be in project root
ls -la .env

# Load explicitly in Python
from dotenv import load_dotenv
load_dotenv()  # Loads from current directory
```

## Best Practices

### 1. Always Activate Virtual Environment
```bash
# Before working on project (uv uses .venv by default)
source .venv/bin/activate

# To deactivate when done
deactivate
```

### 2. Keep Dependencies Updated
```bash
# Check for outdated packages with uv
uv pip list --outdated

# Update specific package
uv pip install --upgrade openai

# Or update all packages
uv pip install --upgrade -r requirements.txt
```

### 3. Why Choose uv?
- **Speed:** 10-100x faster than pip
- **Reliability:** Better dependency resolution
- **Caching:** Intelligent package caching
- **Modern:** Built with Rust for performance
- **Compatible:** Works with pip and PyPI

### 4. Environment Variable Naming
- Use UPPERCASE for environment variables
- Separate words with underscores
- Be descriptive: `OPENAI_API_KEY` not `KEY`

### 5. .gitignore
Ensure these are in .gitignore:
```
.env
venv/
.venv/  # uv virtual environment
__pycache__/
*.pyc
db/
*.json  # Credentials
```

## Verification Checklist

Before moving to Lesson 2, ensure:

- [ ] Virtual environment created and activated
- [ ] All packages from requirements.txt installed
- [ ] .env file created with OPENAI_API_KEY
- [ ] Verification script runs successfully
- [ ] Test embedding generation works
- [ ] No error messages

## Next Steps

Once your environment is set up:

1. ✅ You can create embeddings
2. ✅ You can install Python packages
3. ✅ You understand environment variables
4. ➡️ **Proceed to Lesson 2: Understanding Embeddings**

## Additional Resources

- [uv documentation](https://docs.astral.sh/uv/)
- [uv GitHub repository](https://github.com/astral-sh/uv)
- [Python venv documentation](https://docs.python.org/3/library/venv.html)
- [OpenAI API documentation](https://platform.openai.com/docs)
- [python-dotenv documentation](https://pypi.org/project/python-dotenv/)

## Questions?

- Check `docs/troubleshooting.md` for common issues
- Review `docs/best-practices.md` for coding guidelines
- Ask in project discussions or issues
