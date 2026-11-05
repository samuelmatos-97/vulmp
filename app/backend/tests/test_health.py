def test_health(client):
    """Confirm that the API process is alive."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness(client):
    """Confirm that the API can communicate with PostgreSQL."""

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
