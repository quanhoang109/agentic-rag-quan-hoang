# Lesson 1: Setup Instructions

## Step-by-Step Guide

### Part 1: Create Virtual Environment

**Why?** Virtual environments isolate project dependencies from your system Python.

```bash
# Navigate to project root
cd /path/to/agentic-rag

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### Part 2: Install Dependencies

```bash
# Ensure pip is up to date
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

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

**Verification:**
```bash
pip list | grep openai
# Should show: openai, openai-agents
```

### Part 3: Set Up Environment Variables

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

### Part 4: Verify Installation

Run the verification script:

```bash
python lessons/lesson-01-setup/solution/verify.py
```

**Expected output:**
```
✓ Python version: 3.10.x (OK)
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

### Part 5: Test OpenAI Connection

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

### Issue 1: "pip: command not found"
**Solution:** Ensure Python is installed correctly
```bash
python -m ensurepip --upgrade
```

### Issue 2: "Permission denied"
**Solution:** Use user installation
```bash
pip install --user -r requirements.txt
```

### Issue 3: "ModuleNotFoundError: No module named 'dotenv'"
**Solution:** Virtual environment not activated
```bash
source venv/bin/activate  # Activate first
pip install python-dotenv
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
# Before working on project
source venv/bin/activate

# To deactivate when done
deactivate
```

### 2. Keep Dependencies Updated
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade openai
```

### 3. Environment Variable Naming
- Use UPPERCASE for environment variables
- Separate words with underscores
- Be descriptive: `OPENAI_API_KEY` not `KEY`

### 4. .gitignore
Ensure these are in .gitignore:
```
.env
venv/
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

- [Python venv documentation](https://docs.python.org/3/library/venv.html)
- [pip user guide](https://pip.pypa.io/en/stable/user_guide/)
- [OpenAI API documentation](https://platform.openai.com/docs)
- [python-dotenv documentation](https://pypi.org/project/python-dotenv/)

## Questions?

- Check `docs/troubleshooting.md` for common issues
- Review `docs/best-practices.md` for coding guidelines
- Ask in project discussions or issues
