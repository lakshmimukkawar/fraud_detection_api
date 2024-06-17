import pytest


def test_ping_endpoint(client):
    response = client.get("/ping")
    assert response.status_code == 200
