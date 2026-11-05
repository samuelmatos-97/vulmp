from sqlalchemy import inspect
from sqlalchemy import text


def test_database_setup(test_engine):
    """Verify the isolated database identity and migrated schema."""

    with test_engine.connect() as connection:
        # Confirm the connection uses the test database and user.
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()
        assert database_name == "vulmp_test_db"

        database_user = connection.execute(
            text("SELECT current_user")
        ).scalar_one()
        assert database_user == "vulmp_test"

        # Confirm Alembic applied the expected migration.
        revision = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()
        assert revision == "7783a45490f5"

        # Inspect the table and index without changing data.
        inspector = inspect(connection)
        assert inspector.has_table("assets")

        index_names = {
            index["name"] for index in inspector.get_indexes("assets")
        }
        assert "ix_assets_id" in index_names
