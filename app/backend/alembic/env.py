import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from dotenv import find_dotenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import pool


# Directory containing the backend application and Alembic files.
BACKEND_DIR = Path(__file__).resolve().parents[1]

# Allow Alembic to import the Python package named "app".
sys.path.insert(0, str(BACKEND_DIR))

# Look for a local .env file when Alembic runs outside Docker.
# Inside Docker, the variables are already injected by Docker Compose.
env_file = find_dotenv(filename=".env", usecwd=True)

if env_file:
    load_dotenv(env_file)

# Import the models so SQLAlchemy registers their tables in Base.metadata.
from app import models  # noqa: E402, F401
from app.database import Base  # noqa: E402
from app.database import DATABASE_URL  # noqa: E402


# Read the Alembic configuration from alembic.ini.
config = context.config

# Configure logging using the sections defined in alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic compares this metadata with the real database schema.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Generate migration SQL without opening a database connection."""

    context.configure(
        # Include the real password in the internal connection URL.
        url=DATABASE_URL.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    # Create a migration transaction.
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a real database connection."""

    # Create a dedicated engine without keeping pooled connections.
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        # Apply all migration operations inside a transaction.
        with context.begin_transaction():
            context.run_migrations()


# Alembic selects the correct execution mode automatically.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
