import json
import logging
from pathlib import Path

from pydantic import ValidationError

from falcon_solver.shared import EmpireConfiguration, FalconConfiguration


def parse_json(
    path: str, config: type[EmpireConfiguration] | type[FalconConfiguration]
) -> EmpireConfiguration | FalconConfiguration:

    with open(path, encoding="utf-8") as fn:
        json_falcon = json.loads(fn.read())
    try:
        return config(**json_falcon)
    except ValidationError:
        logging.error("JSON in %s was invalid", path)
        raise


def process_bounty_hunters(bounty_hunters: list[dict]) -> dict[int, list[str]]:
    """
    Preprocess the bounty hunters list into a more accessible dict for quick look up
    Indexed by day to planets
    """
    new: dict[int, list[str]] = {}
    for bh in bounty_hunters:
        planet = bh["planet"]
        day = bh["day"]
        if day not in new:
            new[day] = []
        if planet not in new[day]:
            new[day].append(planet)
    return new
