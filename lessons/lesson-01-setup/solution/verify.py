#!/usr/bin/env python3
"""
Verification script for Lesson 1: Environment Setup
Checks that all dependencies and configuration are correct.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verify Python version is 3.10 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python version: {version.major}.{version.minor}.{version.micro} (Requires 3.10+)")
        return False

def check_virtual_env():
    """Check if uv virtual environment is active."""
    # Check for uv venv or standard venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment: Active")
        return True
    else:
        print("⚠ Virtual environment: Not detected (recommended but optional)")
        return True

def check_uv_installed():
    """Check if uv package manager is installed."""
    import subprocess
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ uv: Installed ({version})")
            return True
        else:
            print("⚠ uv: Not found (install with: pip install uv)")
            return True  # Not mandatory
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("⚠ uv: Not found (install with: pip install uv)")
        return True  # Not mandatory

def check_package(package_name, import_name=None):
    """Check if a package is installed."""
    import_name = import_name or package_name
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✓ {package_name}: Installed (version {version})")
        return True
    except ImportError:
        print(f"✗ {package_name}: Not installed")
        return False

def check_env_file():
    """Check if .env file exists in project root."""
    # Navigate up to project root
    current = Path(__file__).resolve()
    project_root = current.parent.parent.parent.parent
    env_path = project_root / '.env'

    if env_path.exists():
        print("✓ .env file: Found")
        return True, project_root
    else:
        print("✗ .env file: Not found (copy from .env.example)")
        return False, project_root

def check_env_variables(project_root):
    """Check if required environment variables are set."""
    from dotenv import load_dotenv

    # Load .env from project root
    env_path = project_root / '.env'
    load_dotenv(env_path)

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key.startswith("sk-"):
        print("✓ OPENAI_API_KEY: Set")
        return True, openai_key
    else:
        print("✗ OPENAI_API_KEY: Not set or invalid")
        return False, None

def test_openai_connection(api_key):
    """Test connection to OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Test with a simple embedding request
        response = client.embeddings.create(
            input="test",
            model="text-embedding-3-small"
        )

        if len(response.data[0].embedding) == 1536:
            print("✓ OpenAI API: Connection successful")
            print("✓ Embedding test: Passed")
            return True
        else:
            print("✗ Embedding test: Unexpected dimensions")
            return False

    except Exception as e:
        print(f"✗ OpenAI API: Connection failed ({str(e)})")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Environment Setup Verification")
    print("=" * 60)
    print()

    checks = []

    # Check Python version
    checks.append(check_python_version())

    # Check uv package manager
    checks.append(check_uv_installed())

    # Check virtual environment
    checks.append(check_virtual_env())

    # Check required packages
    print()
    print("Checking packages...")
    checks.append(check_package("OpenAI", "openai"))
    checks.append(check_package("OpenAI Agents SDK", "agents"))
    checks.append(check_package("ChromaDB", "chromadb"))
    checks.append(check_package("Flask", "flask"))
    checks.append(check_package("Streamlit", "streamlit"))
    checks.append(check_package("Pandas", "pandas"))
    checks.append(check_package("python-dotenv", "dotenv"))

    # Check .env file
    print()
    print("Checking configuration...")
    env_exists, project_root = check_env_file()
    checks.append(env_exists)

    # Check environment variables
    if env_exists:
        env_valid, api_key = check_env_variables(project_root)
        checks.append(env_valid)

        # Test API connection
        if env_valid and api_key:
            print()
            print("Testing API connection...")
            checks.append(test_openai_connection(api_key))

    # Summary
    print()
    print("=" * 60)
    if all(checks):
        print("✅ All checks passed!")
        print("Your environment is ready for Lesson 2: Understanding Embeddings")
    else:
        print("⚠️  Some checks failed.")
        print("Please review the errors above and fix them.")
        print()
        print("Common fixes:")
        print("  - Install uv: pip install uv")
        print("  - Install packages: uv pip install -r requirements.txt")
        print("  - Or use pip: pip install -r requirements.txt")
        print("  - Create .env file: cp .env.example .env")
        print("  - Add your OpenAI API key to .env file")
    print("=" * 60)

    return all(checks)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
