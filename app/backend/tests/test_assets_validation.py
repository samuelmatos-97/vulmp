import pytest


@pytest.mark.parametrize(
    "field_name",
    ["name", "asset_type", "environment"],
)
def test_create_asset_missing_field(client, field_name):
    """Reject creation when a required field is missing."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    payload.pop(field_name)

    response = client.post("/assets", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert any(
        error["loc"] == ["body", field_name]
        for error in errors
    )

    # Rejected requests must not create an asset.
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "field_name",
    ["name", "asset_type", "environment"],
)
def test_create_asset_null_field(client, field_name):
    """Reject explicit null values in required fields."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    payload[field_name] = None

    response = client.post("/assets", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert any(
        error["loc"] == ["body", field_name]
        for error in errors
    )

    # Rejected requests must not create an asset.
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "field_name",
    ["name", "asset_type"],
)
def test_update_asset_null_field(client, field_name):
    """Reject explicit null without applying any asset changes."""

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]
    expected_asset = {"id": asset_id, **payload}

    # Reject the whole update, including the valid environment change.
    response = client.patch(
        f"/assets/{asset_id}",
        json={
            "environment": "staging",
            field_name: None,
        },
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert any(
        error["loc"] == ["body", field_name]
        for error in errors
    )

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset


@pytest.mark.parametrize(
    "field_name",
    ["name", "asset_type", "environment"],
)
@pytest.mark.parametrize(
    "invalid_value",
    [123, 1.5, True, [], {}],
    ids=["integer", "float", "boolean", "list", "object"],
)
def test_update_asset_invalid_type(client, field_name, invalid_value):
    """Reject invalid field types without changing the asset."""

    # Give each case its own list or dictionary.
    if isinstance(invalid_value, (list, dict)):
        invalid_value = invalid_value.copy()

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]
    expected_asset = {"id": asset_id, **payload}

    response = client.patch(
        f"/assets/{asset_id}",
        json={field_name: invalid_value},
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert any(
        error["loc"][:2] == ["body", field_name]
        and error["type"] == "string_type"
        for error in errors
    )

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset
