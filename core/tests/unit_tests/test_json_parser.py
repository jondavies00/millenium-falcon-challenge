import pytest
from pydantic import ValidationError

from falcon_solver.parser.parse_json import parse_json
from falcon_solver.shared.models import (EmpireConfiguration,
                                         FalconConfiguration)


@pytest.mark.parametrize(
    "test_path,config,expected",
    [
        (
            "/tests/resources/empire-1.json",
            EmpireConfiguration,
            {
                "countdown": 7,
                "bounty_hunters": [
                    {"planet": "Hoth", "day": 6},
                    {"planet": "Hoth", "day": 7},
                    {"planet": "Hoth", "day": 8},
                ],
            },
        ),
        (
            "/tests/resources/millennium-falcon.json",
            FalconConfiguration,
            {
                "autonomy": 6,
                "departure": "Tatooine",
                "arrival": "Endor",
                "routes_db": "/tests/resources/universe.db",
            },
        ),
    ],
)
def test_universe_parser(test_path, config, expected):
    parsed = parse_json(test_path, config)
    assert parsed.dict() == expected


def test_invalid_parse():
    with pytest.raises(ValidationError):
        parsed = parse_json("/tests/resources/invalid-empire.json", EmpireConfiguration)
