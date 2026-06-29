"""
Global constants
"""

from pathlib import Path

CURR_DIR = Path(__file__).parent
ROOT_DIR = CURR_DIR.parent
SRC_DIR = ROOT_DIR / 'source'
POST_DIR = SRC_DIR / '_posts'
BASELINE_FILE = CURR_DIR / 'last_scanned_commit.txt'