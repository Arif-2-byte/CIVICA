"""upgrade attempt answer model

Revision ID: 2cb2649d6944
Revises: 0d3c335ebf7d
Create Date: 2026-08-08 20:48:33.712121
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "2cb2649d6944"
down_revision: Union[str, Sequence[str], None] = "0d3c335ebf7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "attempt_answers",
        "selected_option",
        existing_type=sa.String(length=1),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="selected_option::integer",
    )

    op.alter_column(
        "attempt_answers",
        "is_marked_for_review",
        existing_type=sa.Boolean(),
        nullable=False,
    )

    op.alter_column(
        "attempt_answers",
        "answered_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )

    op.create_index(
        op.f("ix_attempt_answers_attempt_id"),
        "attempt_answers",
        ["attempt_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_attempt_answers_question_id"),
        "attempt_answers",
        ["question_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_attempt_answers_question_id"),
        table_name="attempt_answers",
    )

    op.drop_index(
        op.f("ix_attempt_answers_attempt_id"),
        table_name="attempt_answers",
    )

    op.alter_column(
        "attempt_answers",
        "answered_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )

    op.alter_column(
        "attempt_answers",
        "is_marked_for_review",
        existing_type=sa.Boolean(),
        nullable=True,
    )

    op.alter_column(
        "attempt_answers",
        "selected_option",
        existing_type=sa.Integer(),
        type_=sa.String(length=1),
        existing_nullable=True,
    )