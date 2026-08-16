"""upgrade test model

Revision ID: 2e84b1a96c44
Revises: 4176072e2ad5
Create Date: 2026-08-06 11:45:45.768170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e84b1a96c44"
down_revision: Union[str, Sequence[str], None] = "4176072e2ad5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "tests",
        sa.Column(
            "instructions",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "test_type",
            sa.String(length=30),
            nullable=False,
            server_default="Mock Test",
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "difficulty",
            sa.String(length=20),
            nullable=False,
            server_default="Mixed",
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "language",
            sa.String(length=30),
            nullable=False,
            server_default="English",
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "passing_marks",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "shuffle_questions",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "shuffle_options",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "show_result",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "is_published",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "start_time",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "end_time",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.add_column(
        "tests",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.alter_column(
        "tests",
        "description",
        existing_type=sa.VARCHAR(length=500),
        type_=sa.Text(),
        existing_nullable=True,
    )

    op.alter_column(
        "tests",
        "total_marks",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )

    op.alter_column(
        "tests",
        "negative_marks",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "tests",
        "negative_marks",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        nullable=True,
    )

    op.alter_column(
        "tests",
        "total_marks",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )

    op.alter_column(
        "tests",
        "description",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=500),
        existing_nullable=True,
    )

    op.drop_column("tests", "updated_at")
    op.drop_column("tests", "created_at")
    op.drop_column("tests", "end_time")
    op.drop_column("tests", "start_time")
    op.drop_column("tests", "is_published")
    op.drop_column("tests", "show_result")
    op.drop_column("tests", "shuffle_options")
    op.drop_column("tests", "shuffle_questions")
    op.drop_column("tests", "passing_marks")
    op.drop_column("tests", "language")
    op.drop_column("tests", "difficulty")
    op.drop_column("tests", "test_type")
    op.drop_column("tests", "instructions")