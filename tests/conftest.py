import sys
import os
from pathlib import Path

# Add src to pythonpath so tests can import nexora
# Get the root directory (parent of tests/)
ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR / "src"
sys.path.append(str(SRC_DIR))
