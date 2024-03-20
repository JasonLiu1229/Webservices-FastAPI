from fastapi.testclient import TestClient

from app import app

import pytest

client = TestClient(app)

def test_get_country():
    response = client.get("/api/country")

