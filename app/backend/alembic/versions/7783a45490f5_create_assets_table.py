"""Create the initial assets table.

Revision ID: 7783a45490f5
Revises:
Create Date: 2026-08-04 16:31:22.843695
"""

from typing import Sequence
from typing import Union

from alembic import op
import sqlalchemy as sa


# Unique identifier of this migration.
revision: str = "7783a45490f5"

# This is the first migration, so it has no previous revision.
down_revision: Union[str, Sequence[str], None] = None

# These fields are not needed for this migration.
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Defines what happens when the migration is applied (upgrade).
def upgrade() -> None:
    """Create the assets table."""

    # Create the table that stores the managed assets.
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("asset_type", sa.String(), nullable=False),
        sa.Column("environment", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create the index defined by index=True in the Asset model.
    op.create_index(
        "ix_assets_id",
        "assets",
        ["id"],
        unique=False,
    )

# Defines what happens when the migration is rolled back (downgrade).
def downgrade() -> None:
    """Remove the assets table."""

    # Remove the index before removing the table.
    op.drop_index(
        "ix_assets_id",
        table_name="assets",
    )

    # Remove the assets table.
    op.drop_table("assets")
