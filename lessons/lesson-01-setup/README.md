# Lesson 1: Environment Setup & Prerequisites

## Overview
Set up your development environment and verify all tools are properly configured for building the multi-agent RAG system.

## Learning Objectives
By the end of this lesson, you will:
- Install and use uv, a modern fast Python package manager
- Create and activate a Python virtual environment with uv
- Install all required dependencies (10-100x faster than pip!)
- Configure API keys and environment variables
- Verify your setup is working correctly

## Duration
20-30 minutes (faster with uv!)

## Prerequisites
- Python 3.10 or higher installed
- Basic command line knowledge
- Text editor (VS Code, PyCharm, or similar)
- pip (comes with Python)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- OpenRouter API key ([Get one here](https://openrouter.ai/keys)) - optional

## Topics Covered
1. Modern package management with uv
2. Python virtual environments (with uv)
3. Fast dependency installation
4. Environment variables and .env files
5. API key management best practices

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
- ✅ uv package manager installed
- ✅ Virtual environment (`.venv`)
- ✅ Installed dependencies (fast!)
- ✅ `.env` file with API keys
- ✅ Verification script that confirms setup

## Files in This Lesson
- `README.md` - This overview
- `instructions.md` - Step-by-step setup guide
- `solution/verify.py` - Script to verify installation
- `solution/.env.example` - Template for environment variables

## Next Steps
After completing this lesson, proceed to Lesson 2: Understanding Embeddings

## Why uv?

**uv** is a modern Python package manager developed by Astral (creators of Ruff):
- ⚡ **10-100x faster** than pip
- 🔒 **Reliable** dependency resolution
- 🚀 **Written in Rust** for maximum performance
- 💾 **Smart caching** for faster reinstalls
- 🔄 **100% compatible** with pip and PyPI

**Installation time comparison:**
- pip: ~2-3 minutes for all dependencies
- uv: ~10-20 seconds for all dependencies

## Troubleshooting
If you encounter issues, check:
- Python version is correct (3.10+)
- uv is installed (`uv --version`)
- Virtual environment is activated
- API keys are valid
- No typos in .env file

For more help, see `docs/troubleshooting.md`
