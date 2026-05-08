
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from main import build_app


if __name__ == "__main__":
    build_app().run()
