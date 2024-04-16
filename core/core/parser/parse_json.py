import json
import logging
from typing import Literal

from pydantic import ValidationError

from core.shared import EmpireConfiguration, FalconConfiguration


def parse_json(
    path: str, config: type[EmpireConfiguration] | type[FalconConfiguration]
) -> EmpireConfiguration | FalconConfiguration:

    with open(path) as fn:
        json_falcon = json.loads(fn.read())
        logging.info(json_falcon)
    try:
        return config(**json_falcon)
    except ValidationError as exc:
        logging.error("JSON in %s was invalid" % path)
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
        if day not in bh:
            new[day] = []
        if planet not in new[day]:
            new[day].append(planet)
    return new
