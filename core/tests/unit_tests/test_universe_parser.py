import logging

from falcon_solver.parser.parse_universe import parse_universe


def test_universe_parser():
    parsed = parse_universe("tests/resources/universe.db")
    assert parsed == {
        "Tatooine": {"Dagobah": 6, "Hoth": 6},
        "Dagobah": {"Tatooine": 6, "Endor": 4, "Hoth": 1},
        "Endor": {"Dagobah": 4, "Hoth": 1},
        "Hoth": {"Dagobah": 1, "Endor": 1, "Tatooine": 6},
    }
