import pytest
from pydantic import ValidationError

from falcon_solver.parser.parse_json import parse_json, process_bounty_hunters
from falcon_solver.shared.models import EmpireConfiguration, FalconConfiguration


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


def test_invalid_empire_parse():
    with pytest.raises(ValidationError):
        parse_json("/tests/resources/invalid-empire.json", EmpireConfiguration)


def test_invalid_millennium_falcon_parse():
    """
    Ensures negative numbers raise validation errors
    """
    with pytest.raises(ValidationError):
        parse_json(
            "/tests/resources/invalid-millennium-falcon.json", FalconConfiguration
        )


def test_parse_bounty_hunters():
    parsed = process_bounty_hunters(
        [
            {"planet": "Hoth", "day": 2},
            {"planet": "Hoth", "day": 3},
            {"planet": "Hoth", "day": 4},
            {"planet": "Hoth", "day": 5},
            {"planet": "Hoth", "day": 6},
            {"planet": "Hoth", "day": 7},
            {"planet": "Hoth", "day": 8},
            {"planet": "Dagobah", "day": 8},
            {"planet": "Dagobah", "day": 7},
            {"planet": "Dagobah", "day": 6},
            {"planet": "Dagobah", "day": 5},
        ]
    )
    assert parsed == {
        2: ["Hoth"],
        3: ["Hoth"],
        4: ["Hoth"],
        5: ["Hoth", "Dagobah"],
        6: ["Hoth", "Dagobah"],
        7: ["Hoth", "Dagobah"],
        8: ["Hoth", "Dagobah"],
    }
