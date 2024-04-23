from pydantic import BaseModel


class OddsModel(BaseModel):
    odds: int
    route: list[str]
