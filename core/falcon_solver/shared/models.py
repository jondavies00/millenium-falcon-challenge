from dataclasses import dataclass
from pydantic import BaseModel, field_validator
import logging

@dataclass
class PathStep:
    autonomy: int
    day: int
    route: list[str]
    seen_bounty_hunters: int


class FalconConfiguration(BaseModel):
    autonomy: int
    departure: str
    arrival: str
    routes_db: str


class EmpireConfiguration(BaseModel):
    countdown: int
    bounty_hunters: list[dict[str, str | int]]

    @field_validator('bounty_hunters', mode="before")
    @classmethod
    def bounty_hunters_types(cls, v: list[dict]) -> str:
        for bounty_hunter_dict in v:
            bounty_hunter_dict["day"] = int(bounty_hunter_dict["day"])
        return v
