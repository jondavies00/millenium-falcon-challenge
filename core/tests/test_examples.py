import logging

import pytest

from falcon_solver.parser.parse_json import parse_json
from falcon_solver.shared.models import (EmpireConfiguration,
                                         FalconConfiguration)
from falcon_solver.solver.solver import Solver


@pytest.mark.parametrize(
    "empire_filename,odds",
    [("empire-1", 0), ("empire-2", 81), ("empire-3", 90), ("empire-4", 100)],
)
def test_examples(empire_filename: str, odds: float):
    solver = Solver(
        falcon_config=parse_json(
            "/tests/resources/millennium-falcon.json", FalconConfiguration
        ),
        empire_config=parse_json(
            f"/tests/resources/{empire_filename}.json", EmpireConfiguration
        ),
    )
    assert odds == solver.tell_me_the_odds(rounded=True)
