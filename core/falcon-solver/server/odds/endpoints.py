from fastapi import APIRouter
from ..models import OddsModel

router = APIRouter(tags=["Odds Calculations"], prefix="/odds")

@router.get("", response_model=OddsModel)
async def odds():
    return OddsModel(odds=1, route=["test"])
