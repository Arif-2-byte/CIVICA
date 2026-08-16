"""upgrade test question model

Revision ID: c6db1559a84a
Revises: 2e84b1a96c44
Create Date: 2026-08-08 16:43:47.852924

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6db1559a84a"
down_revision: Union[str, Sequence[str], None] = "2e84b1a96c44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "test_questions",
        sa.Column(
            "section_name",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "test_questions",
        sa.Column(
            "marks_override",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "test_questions",
        sa.Column(
            "negative_marks_override",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "test_questions",
        sa.Column(
            "is_mandatory",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.create_index(
        op.f("ix_test_questions_question_id"),
        "test_questions",
        ["question_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_test_questions_test_id"),
        "test_questions",
        ["test_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_test_questions_test_id"),
        table_name="test_questions",
    )

    op.drop_index(
        op.f("ix_test_questions_question_id"),
        table_name="test_questions",
    )

    op.drop_column(
        "test_questions",
        "is_mandatory",
    )

    op.drop_column(
        "test_questions",
        "negative_marks_override",
    )

    op.drop_column(
        "test_questions",
        "marks_override",
    )

    op.drop_column(
        "test_questions",
        "section_name",
    )