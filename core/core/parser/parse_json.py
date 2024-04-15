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
