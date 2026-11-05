def test_update_asset_one_field(client):
    """Update one field and preserve the remaining asset fields."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]

    updates = {"environment": "staging"}
    expected_asset = {"id": asset_id, **payload, **updates}

    response = client.patch(f"/assets/{asset_id}", json=updates)

    assert response.status_code == 200
    assert response.json() == expected_asset

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset


def test_update_asset_multiple_fields(client):
    """Update multiple fields and preserve omitted fields."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]

    updates = {
        "name": "renamed-server-01",
        "environment": "staging",
    }
    expected_asset = {"id": asset_id, **payload, **updates}

    response = client.patch(f"/assets/{asset_id}", json=updates)

    assert response.status_code == 200
    assert response.json() == expected_asset

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset


def test_update_asset_empty_payload(client):
    """Accept an empty update without changing the asset."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]
    expected_asset = {"id": asset_id, **payload}

    response = client.patch(f"/assets/{asset_id}", json={})

    assert response.status_code == 200
    assert response.json() == expected_asset

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset


def test_update_asset_null_rejected(client):
    """Reject explicit null without changing any asset fields."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]
    expected_asset = {"id": asset_id, **payload}

    # A valid field must also remain unchanged when validation fails.
    response = client.patch(
        f"/assets/{asset_id}",
        json={
            "name": "should-not-change",
            "environment": None,
        },
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert any(
        error["loc"] == ["body", "environment"]
        for error in errors
    )

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset


def test_update_asset_not_found(client):
    """Return 404 without creating an asset."""

    # Establish that the valid lookup ID cannot match an existing asset.
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []

    response = client.patch(
        "/assets/0",
        json={"environment": "staging"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Asset not found."}

    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []
