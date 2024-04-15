import logging
from core.parser.parse_json import parse_json
from core.solver.solver import Solver
from core.shared.models import (
    FalconConfiguration,
    EmpireConfiguration,
)


def test_example_one():
    custom_config = Solver(
        falcon_config=parse_json(
            "tests/resources/millennium-falcon.json", FalconConfiguration
        ),
        empire_config=parse_json("tests/resources/empire.json", EmpireConfiguration),
    )
    success = custom_config.solve()
    logging.info("Successful: %s", success)
