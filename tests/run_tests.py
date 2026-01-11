"""
Simple test runner script for LLM tests.
Run this to execute all LLM unit tests.
"""

import subprocess
import sys
import os

def run_tests():
    """Run all LLM tests using pytest."""
    try:
        # Get the project root directory (parent of tests/)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=short"],
            cwd=project_root
        )
        return result.returncode
    except FileNotFoundError:
        print("❌ Error: pytest not found. Install with: pip install pytest")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)

