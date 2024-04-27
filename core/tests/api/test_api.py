import json
import logging
from http.client import HTTPException

import pytest
from fastapi.testclient import TestClient


def test_api(client: TestClient):
    resp = client.post(
        "/odds",
        json={
            "empire_config": {
                "countdown": 8,
                "bounty_hunters": [
                    {"planet": "Hoth", "day": 6},
                    {"planet": "Hoth", "day": 7},
                    {"planet": "Hoth", "day": 8},
                ],
            }
        },
    )
    assert resp.json() == 81.0


def test_api_invalid(client: TestClient):
    resp = client.post(
        "/odds",
        json={
            "empire_conffig": {
                "countdown": 8,
                "bounty_hunters": [
                    {"planet": "Hoth", "day": 6},
                    {"planet": "Hoth", "day": 7},
                    {"planet": "Hoth", "day": 8},
                ],
            }
        },
    )
    assert resp.status_code == 422


def test_api_big_countdown(client: TestClient):
    """
    Test a potentially long request
    """
    resp = client.post(
        "/odds",
        json={
            "empire_config": {
                "countdown": 1000,
                "bounty_hunters": [
                    {"planet": "Hoth", "day": 6},
                    {"planet": "Hoth", "day": 7},
                    {"planet": "Hoth", "day": 8},
                ],
            }
        },
    )
    assert resp.json() == 100
