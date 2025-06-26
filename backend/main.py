import sys
from pathlib import Path

import logfire

root_path = Path(__file__).resolve().parent
sys.path.append(str(root_path))


from api import health_router
from fastapi import FastAPI

logfire.configure()
logfire.instrument_pydantic_ai()

app = FastAPI()

app.include_router(health_router)
