#!/usr/bin/env python3
"""
Ensure data/archive/ exists for newsletter history tracking.

Upload past newsletter HTML files to data/archive/ so that
check_history.py can detect URLs already published in previous issues.

Usage:
    python scripts/setup_db.py
"""
from pathlib import Path

ARCHIVE_DIR = Path(__file__).parent.parent / "data" / "archive"


def main():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    files = list(ARCHIVE_DIR.glob("*.html"))
    print(f"Archive ready: {ARCHIVE_DIR}")
    if files:
        print(f"  {len(files)} past newsletter(s) loaded for history checking:")
        for f in sorted(files):
            print(f"    - {f.name}")
    else:
        print("  No past newsletters yet. Upload newsletter HTML files to data/archive/")
        print("  to enable duplicate detection across issues.")


if __name__ == "__main__":
    main()
