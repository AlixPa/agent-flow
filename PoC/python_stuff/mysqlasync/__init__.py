import os
import sys
from pathlib import Path

import logfire
from dotenv import load_dotenv

REPO_ROOT_PATH = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=REPO_ROOT_PATH / ".env", override=False)

mysql_port_local = os.getenv("MYSQL_PORT_LOCAL")
if mysql_port_local:
    os.environ["MYSQL_PORT"] = mysql_port_local

sys.path.append(str(REPO_ROOT_PATH / "backend"))

import src

logfire.configure()
logfire.instrument_pydantic_ai()
