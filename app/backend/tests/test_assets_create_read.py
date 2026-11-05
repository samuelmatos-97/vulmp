def test_create_asset(client):
    """Create an asset and return its public fields."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }

    response = client.post("/assets", json=payload)

    assert response.status_code == 200
    created_asset = response.json()
    assert type(created_asset["id"]) is int
    assert created_asset == {"id": created_asset["id"], **payload}


def test_get_asset(client):
    """Retrieve the asset created during this test."""

    payload = {
        "name": "api-server-01",
        "asset_type": "server",
        "environment": "staging",
    }

    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]

    response = client.get(f"/assets/{asset_id}")

    assert response.status_code == 200
    assert response.json() == {"id": asset_id, **payload}


def test_list_assets(client):
    """Return all assets created during this test."""

    payloads = [
        {
            "name": "web-server-01",
            "asset_type": "server",
            "environment": "test",
        },
        {
            "name": "database-01",
            "asset_type": "database",
            "environment": "staging",
        },
    ]
    expected_assets = []

    for payload in payloads:
        create_response = client.post("/assets", json=payload)
        assert create_response.status_code == 200
        asset_id = create_response.json()["id"]
        expected_assets.append({"id": asset_id, **payload})

    response = client.get("/assets")

    assert response.status_code == 200
    assets = response.json()
    assert isinstance(assets, list)
    assert len(assets) == len(expected_assets)

    # The API does not promise collection order.
    for expected_asset in expected_assets:
        assert expected_asset in assets


def test_list_assets_empty(client):
    """Return an empty list when this test creates no assets."""

    response = client.get("/assets")

    assert response.status_code == 200
    assert response.json() == []


def test_get_asset_not_found(client):
    """Return 404 when a valid ID has no matching asset."""

    # Confirm the collection is empty before choosing an absent ID.
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get("/assets/0")

    assert response.status_code == 404
    assert response.json() == {"detail": "Asset not found."}
