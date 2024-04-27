import pytest
from fastapi.testclient import TestClient

from falcon_solver.server.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app=create_app())
