import os
import sys
from pathlib import Path

from dotenv import load_dotenv

root_path = Path(__file__).resolve().parent
sys.path.append(str(root_path))

load_dotenv(override=False)

ENV = os.getenv("ENV", "local")


class ServiceEnv:
    LOCAL = "local"
    PRODUCTION = "production"
