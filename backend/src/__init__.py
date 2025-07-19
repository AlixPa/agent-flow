from pathlib import Path

import logfire
from dotenv import load_dotenv

REPO_ROOT_PATH = Path(__file__).resolve().parents[2]
load_dotenv(
    dotenv_path=REPO_ROOT_PATH / ".env",
    override=False,
)
logfire.configure()
logfire.instrument_pydantic_ai()
