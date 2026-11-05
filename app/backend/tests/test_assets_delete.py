def test_delete_asset(client):
    """Delete an asset and return 404 for later requests."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]

    response = client.delete(f"/assets/{asset_id}")

    assert response.status_code == 204
    assert response.content == b""

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Asset not found."}

    response = client.delete(f"/assets/{asset_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Asset not found."}

    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []


def test_delete_asset_not_found(client):
    """Return 404 without changing an empty collection."""

    # Establish that the valid lookup ID cannot match an existing asset.
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []

    response = client.delete("/assets/0")

    assert response.status_code == 404
    assert response.json() == {"detail": "Asset not found."}

    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []


def test_delete_asset_preserves_other_assets(client):
    """Delete one asset without changing the other."""

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
    created_assets = []

    for payload in payloads:
        create_response = client.post("/assets", json=payload)
        assert create_response.status_code == 200
        asset_id = create_response.json()["id"]
        created_assets.append({"id": asset_id, **payload})

    deleted_asset, remaining_asset = created_assets

    response = client.delete(f"/assets/{deleted_asset['id']}")

    assert response.status_code == 204
    assert response.content == b""

    response = client.get(f"/assets/{remaining_asset['id']}")
    assert response.status_code == 200
    assert response.json() == remaining_asset

    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == [remaining_asset]
