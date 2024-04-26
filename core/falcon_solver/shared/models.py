import logging
from dataclasses import dataclass
from typing import TypedDict

from pydantic import BaseModel, root_validator


@dataclass
class PathStep:
    autonomy: int
    day: int
    route: list[str]
    seen_bounty_hunters: int

class BountyHunters(TypedDict):
    day: int
    planet: str

class FalconConfiguration(BaseModel):
    autonomy: int
    departure: str
    arrival: str
    routes_db: str

class EmpireConfiguration(BaseModel):
    countdown: int
    # coerces potentially json-loaded bounty hunters into correct types
    bounty_hunters: list[BountyHunters] 