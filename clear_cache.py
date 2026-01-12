"""
Clear Python cache files.
Run this when you make changes and they don't seem to take effect.
"""

import os
import shutil
from pathlib import Path

def clear_pycache(root_dir="."):
    """Remove all __pycache__ directories."""
    root_path = Path(root_dir)
    count = 0
    
    for pycache_dir in root_path.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            print(f"[OK] Cleared: {pycache_dir}")
            count += 1
        except Exception as e:
            print(f"[FAIL] Failed to clear {pycache_dir}: {e}")
    
    print(f"\n[SUCCESS] Cleared {count} cache directories")

if __name__ == "__main__":
    clear_pycache()

