from pydantic import BaseModel


class OddsModel(BaseModel):
    odds: int
    route: list[str]

class CalculateOddsRequestModel(BaseModel):
    empire_json: dict
