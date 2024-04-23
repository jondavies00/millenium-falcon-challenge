from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class PathStep:
    autonomy: int
    day: int
    route: list[str]


class FalconConfiguration(BaseModel):
    autonomy: int
    departure: str
    arrival: str
    routes_db: str


class EmpireConfiguration(BaseModel):
    countdown: int
    bounty_hunters: list[dict[str, str | int]]
