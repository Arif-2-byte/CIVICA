"""upgrade test attempt model

Revision ID: 0d3c335ebf7d
Revises: c6db1559a84a
Create Date: 2026-08-08 20:28:54.128272

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0d3c335ebf7d"
down_revision: Union[str, Sequence[str], None] = "c6db1559a84a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "test_attempts",
        "score",
        existing_type=sa.Integer(),
        type_=sa.Float(),
        nullable=False,
    )

    op.alter_column(
        "test_attempts",
        "total_correct",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "test_attempts",
        "total_wrong",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "test_attempts",
        "total_skipped",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "test_attempts",
        "status",
        existing_type=sa.String(length=20),
        nullable=False,
    )

    op.alter_column(
        "test_attempts",
        "started_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )

    op.create_index(
        op.f("ix_test_attempts_test_id"),
        "test_attempts",
        ["test_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_test_attempts_user_id"),
        "test_attempts",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_test_attempts_user_id"),
        table_name="test_attempts",
    )

    op.drop_index(
        op.f("ix_test_attempts_test_id"),
        table_name="test_attempts",
    )

    op.alter_column(
        "test_attempts",
        "started_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )

    op.alter_column(
        "test_attempts",
        "status",
        existing_type=sa.String(length=20),
        nullable=True,
    )

    op.alter_column(
        "test_attempts",
        "total_skipped",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.alter_column(
        "test_attempts",
        "total_wrong",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.alter_column(
        "test_attempts",
        "total_correct",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.alter_column(
        "test_attempts",
        "score",
        existing_type=sa.Float(),
        type_=sa.Integer(),
        nullable=True,
    )