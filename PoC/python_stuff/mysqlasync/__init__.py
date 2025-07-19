import sys
from pathlib import Path

import logfire

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent / "backend"
sys.path.append(str(ROOT_PATH))

import _config

logfire.configure()
logfire.instrument_pydantic_ai()
