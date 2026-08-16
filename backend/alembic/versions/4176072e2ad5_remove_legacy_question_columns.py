"""remove legacy question columns

Revision ID: 4176072e2ad5
Revises: 7b53b3e6420a
Create Date: 2026-08-03 16:30:18.813921
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "4176072e2ad5"
down_revision: Union[str, Sequence[str], None] = "7b53b3e6420a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Drop legacy question columns
    op.drop_column("questions", "option_a")
    op.drop_column("questions", "option_b")
    op.drop_column("questions", "option_c")
    op.drop_column("questions", "option_d")
    op.drop_column("questions", "correct_option")

    # Drop tags only if it still exists
    try:
        op.drop_column("questions", "tags")
    except Exception:
        pass


def downgrade() -> None:

    op.add_column(
        "questions",
        sa.Column(
            "option_a",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "questions",
        sa.Column(
            "option_b",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "questions",
        sa.Column(
            "option_c",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "questions",
        sa.Column(
            "option_d",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "questions",
        sa.Column(
            "correct_option",
            sa.String(length=1),
            nullable=True,
        ),
    )

    op.add_column(
        "questions",
        sa.Column(
            "tags",
            sa.String(length=500),
            nullable=True,
        ),
    )