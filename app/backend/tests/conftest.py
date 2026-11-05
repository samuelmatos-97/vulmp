import os
import sys

import pytest


EXPECTED_ENVIRONMENT = {
    "VULMP_TESTING": "1",
    "POSTGRES_HOST": "postgres-test",
    "POSTGRES_PORT": "5432",
    "POSTGRES_DB": "vulmp_test_db",
    "POSTGRES_USER": "vulmp_test",
}

DATABASE_MODULES = (
    "app.database",
    "app.models",
    "app.main",
)


def _validate_test_configuration() -> None:
    """Reject unsafe settings before importing database modules."""

    # Reject cached configuration instead of trying to repair it.
    loaded_modules = [
        name for name in DATABASE_MODULES if name in sys.modules
    ]

    if loaded_modules:
        raise pytest.UsageError(
            "Unsafe test startup: application modules were imported "
            "before configuration validation: "
            f"{', '.join(loaded_modules)}. "
            "Start pytest in a fresh process without early application imports."
        )

    # Accept only the exact isolated test configuration.
    for name, expected in EXPECTED_ENVIRONMENT.items():
        if os.environ.get(name) != expected:
            raise pytest.UsageError(
                f"Unsafe test configuration: {name} must equal {expected!r}."
            )

    # Validate the password without displaying or changing it.
    if not os.environ.get("POSTGRES_PASSWORD", "").strip():
        raise pytest.UsageError(
            "Unsafe test configuration: POSTGRES_PASSWORD must be "
            "nonempty and contain a non-whitespace character. "
            "Its value is hidden."
        )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Validate database settings before collecting API tests."""

    _validate_test_configuration()


@pytest.fixture(scope="session")
def test_engine():
    """Apply migrations to the isolated PostgreSQL test database."""

    # Recheck configuration immediately before application imports.
    _validate_test_configuration()

    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    from app import database

    engine = database.engine

    try:
        # Inspect the engine without opening a connection.
        url = engine.url
        expected_destination = {
            "drivername": "postgresql+psycopg",
            "host": EXPECTED_ENVIRONMENT["POSTGRES_HOST"],
            "port": int(EXPECTED_ENVIRONMENT["POSTGRES_PORT"]),
            "database": EXPECTED_ENVIRONMENT["POSTGRES_DB"],
            "username": EXPECTED_ENVIRONMENT["POSTGRES_USER"],
        }

        for field, expected in expected_destination.items():
            if getattr(url, field) != expected:
                raise pytest.UsageError(
                    f"Unsafe test engine: {field} must equal {expected!r}."
                )

        # Prevent additional URL options from changing the destination.
        if url.query:
            raise pytest.UsageError(
                "Unsafe test engine: URL query options are not allowed."
            )

        # Alembic must use the same validated connection configuration.
        if database.DATABASE_URL != url:
            raise pytest.UsageError(
                "Unsafe migration configuration: DATABASE_URL does not "
                "match the validated test engine."
            )

        backend_dir = Path(__file__).resolve().parents[1]
        alembic_config = Config(str(backend_dir / "alembic.ini"))

        # Apply the existing migration history before dependent tests run.
        command.upgrade(alembic_config, "head")

        yield engine

    finally:
        # Release pooled connections without removing schemas or data.
        engine.dispose()


@pytest.fixture(scope="function")
def db_connection(test_engine):
    """Keep one test's database changes inside an outer transaction."""

    with test_engine.connect() as connection:
        transaction = connection.begin()

        try:
            yield connection
        finally:
            transaction.rollback()


@pytest.fixture(scope="function")
def client(db_connection):
    """Provide an API client with isolated database sessions."""

    from fastapi.testclient import TestClient

    from app.database import SessionLocal
    from app.database import get_db
    from app.main import app

    saved_overrides = app.dependency_overrides.copy()

    def override_get_db():
        """Provide one request session inside the test transaction."""

        with SessionLocal(
            bind=db_connection,
            join_transaction_mode="create_savepoint",
        ) as session:
            yield session

    try:
        # Replace the original dependency before starting the client.
        app.dependency_overrides[get_db] = override_get_db

        # Preserve the real application startup and shutdown.
        with TestClient(app) as test_client:
            yield test_client

    finally:
        # Restore all overrides, including after startup or request errors.
        app.dependency_overrides.clear()
        app.dependency_overrides.update(saved_overrides)
