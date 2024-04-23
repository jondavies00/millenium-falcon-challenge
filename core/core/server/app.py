"""
Exposes endpoints to get the odds for some inputs
"""

from fastapi import FastAPI

from core.core.server.models import OddsModel


app = FastAPI()


@app.get("/odds", response_model=OddsModel)
async def odds():
    return OddsModel(odds=1, route=["test"])
