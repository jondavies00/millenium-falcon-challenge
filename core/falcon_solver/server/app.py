"""
Exposes endpoints to get the odds for some inputs
"""

import uvicorn
from fastapi import FastAPI

from .odds.endpoints import router as odds_router


def create_app():
    app = FastAPI()
    app.include_router(odds_router)
    return app


def start_server():
    uvicorn.run("falcon_solver.server.app:create_app", port=8000)
