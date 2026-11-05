import pytest


@pytest.mark.parametrize(
    "method",
    ["GET", "PATCH", "DELETE"],
)
@pytest.mark.parametrize(
    "asset_id",
    [-2147483648, 2147483647],
    ids=["minimum", "maximum"],
)
def test_asset_id_valid_boundaries(client, method, asset_id):
    """Return 404 for absent IDs at the valid integer boundaries."""

    # Establish that the boundary ID is absent.
    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []

    request_kwargs = {}

    # Keep PATCH body validation separate from the path check.
    if method == "PATCH":
        request_kwargs["json"] = {"environment": "staging"}

    response = client.request(
        method,
        f"/assets/{asset_id}",
        **request_kwargs,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Asset not found."}

    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "method",
    ["GET", "PATCH", "DELETE"],
)
@pytest.mark.parametrize(
    "asset_id",
    ["-2147483649", "2147483648", "abc", "1.5"],
    ids=["below-minimum", "above-maximum", "non-integer", "decimal"],
)
def test_asset_id_invalid_values(client, method, asset_id):
    """Reject out-of-range and malformed asset IDs."""

    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []

    request_kwargs = {}

    # Keep PATCH body validation separate from the path check.
    if method == "PATCH":
        request_kwargs["json"] = {"environment": "staging"}

    response = client.request(
        method,
        f"/assets/{asset_id}",
        **request_kwargs,
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert any(
        error["loc"][:2] == ["path", "asset_id"]
        for error in errors
    )

    response = client.get("/assets")
    assert response.status_code == 200
    assert response.json() == []
