import pytest

from falcon_solver.parser.parse_json import parse_json
from falcon_solver.shared.models import EmpireConfiguration, FalconConfiguration
from falcon_solver.solver.solver import Solver


@pytest.mark.parametrize("empire_filename,odds", [("custom_empire", 73)])
def test_custom(empire_filename: str, odds: float):
    """
    Tests when there are bounty hunters on the last planet.
    We apply this as an assumption that we can still be attacked there.
    """
    solver = Solver(
        falcon_config=parse_json(
            "/tests/resources/millennium-falcon.json", FalconConfiguration
        ),
        empire_config=parse_json(
            f"/tests/resources/{empire_filename}.json", EmpireConfiguration
        ),
    )
    assert odds == solver.tell_me_the_odds(rounded=True)
