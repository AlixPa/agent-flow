import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent
sys.path.append(str(root_path))


from api import health_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(health_router)
