import pytest


@pytest.mark.parametrize(
    "asset_name",
    ["isolation-first", "isolation-second"],
)
def test_asset_transaction_isolation(client, asset_name):
    """Verify that each test starts without another test's assets."""

    # Detect data left behind by a previous test.
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []

    # Exercise the endpoint's commit inside the outer transaction.
    response = client.post(
        "/assets",
        json={
            "name": asset_name,
            "asset_type": "server",
            "environment": "test",
        },
    )
    assert response.status_code == 200
    created_asset = response.json()

    # A separate request must see this test's asset.
    response = client.get(f"/assets/{created_asset['id']}")
    assert response.status_code == 200
    assert response.json() == created_asset
