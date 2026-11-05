from unittest.mock import Mock

from sqlalchemy.exc import SQLAlchemyError


def test_update_asset_commit_failure(client, db_connection, monkeypatch):
    """Return HTTP 500 and roll back a failed asset update."""

    from app.database import SessionLocal
    from app.database import get_db
    from app.main import app

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]
    expected_asset = {"id": asset_id, **payload}

    with SessionLocal(
        bind=db_connection,
        join_transaction_mode="create_savepoint",
    ) as db:
        rollback_spy = Mock(wraps=db.rollback)
        commit_failure = Mock(
            side_effect=SQLAlchemyError("Simulated commit failure.")
        )

        def failing_get_db():
            """Provide the real session for the failing request."""
            yield db

        # Limit the injected failure to this request's session.
        with monkeypatch.context() as patch:
            patch.setattr(db, "commit", commit_failure)
            patch.setattr(db, "rollback", rollback_spy)
            patch.setitem(app.dependency_overrides, get_db, failing_get_db)

            response = client.patch(
                f"/assets/{asset_id}",
                json={"environment": "staging"},
            )

        assert response.status_code == 500
        assert response.json() == {"detail": "Database operation failed."}
        commit_failure.assert_called_once_with()
        rollback_spy.assert_called_once_with()

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset


def test_delete_asset_commit_failure(client, db_connection, monkeypatch):
    """Return HTTP 500 and roll back a failed asset deletion."""

    from app.database import SessionLocal
    from app.database import get_db
    from app.main import app

    payload = {
        "name": "web-server-01",
        "asset_type": "server",
        "environment": "test",
    }
    create_response = client.post("/assets", json=payload)
    assert create_response.status_code == 200
    asset_id = create_response.json()["id"]
    expected_asset = {"id": asset_id, **payload}

    with SessionLocal(
        bind=db_connection,
        join_transaction_mode="create_savepoint",
    ) as db:
        rollback_spy = Mock(wraps=db.rollback)
        commit_failure = Mock(
            side_effect=SQLAlchemyError("Simulated commit failure.")
        )

        def failing_get_db():
            """Provide the real session for the failing request."""
            yield db

        # Limit the injected failure to this request's session.
        with monkeypatch.context() as patch:
            patch.setattr(db, "commit", commit_failure)
            patch.setattr(db, "rollback", rollback_spy)
            patch.setitem(app.dependency_overrides, get_db, failing_get_db)

            response = client.delete(f"/assets/{asset_id}")

        assert response.status_code == 500
        assert response.json() == {"detail": "Database operation failed."}
        commit_failure.assert_called_once_with()
        rollback_spy.assert_called_once_with()

    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json() == expected_asset


def test_readiness_database_failure(client, monkeypatch):
    """Return HTTP 503 on connection failure and recover afterward."""

    from app import main

    connection_failure = Mock(
        side_effect=SQLAlchemyError("Simulated connection failure.")
    )
    failing_engine = Mock(connect=connection_failure)

    # Replace only the engine reference used by this request.
    with monkeypatch.context() as patch:
        patch.setattr(main, "engine", failing_engine)
        response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable."}
    connection_failure.assert_called_once_with()

    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
