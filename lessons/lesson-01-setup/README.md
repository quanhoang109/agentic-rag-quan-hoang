# Lesson 1: Environment Setup & Prerequisites

## Overview
Set up your development environment and verify all tools are properly configured for building the multi-agent RAG system.

## Learning Objectives
By the end of this lesson, you will:
- Create and activate a Python virtual environment
- Install all required dependencies
- Configure API keys and environment variables
- Verify your setup is working correctly

## Duration
30 minutes

## Prerequisites
- Python 3.10 or higher installed
- Basic command line knowledge
- Text editor (VS Code, PyCharm, or similar)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- OpenRouter API key ([Get one here](https://openrouter.ai/keys)) - optional

## Topics Covered
1. Python virtual environments
2. Package management with pip
3. Environment variables and .env files
4. API key management best practices

## Getting Started

### Step 1: Check Python Version
```bash
python --version  # Should be 3.10 or higher
```

### Step 2: Clone/Navigate to Repository
```bash
cd /path/to/agentic-rag
```

### Step 3: Follow Instructions
Open `instructions.md` in this directory for detailed step-by-step setup guide.

## What You'll Create
- ✅ Virtual environment
- ✅ Installed dependencies
- ✅ `.env` file with API keys
- ✅ Verification script that confirms setup

## Files in This Lesson
- `README.md` - This overview
- `instructions.md` - Step-by-step setup guide
- `solution/verify.py` - Script to verify installation
- `solution/.env.example` - Template for environment variables

## Next Steps
After completing this lesson, proceed to Lesson 2: Understanding Embeddings

## Troubleshooting
If you encounter issues, check:
- Python version is correct
- Virtual environment is activated
- API keys are valid
- No typos in .env file

For more help, see `docs/troubleshooting.md`
