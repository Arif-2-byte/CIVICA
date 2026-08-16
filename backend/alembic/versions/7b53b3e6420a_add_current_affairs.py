"""add current affairs

Revision ID: 7b53b3e6420a
Revises: 1cbeeee9daeb
Create Date: 2026-08-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "7b53b3e6420a"
down_revision: Union[str, Sequence[str], None] = "1cbeeee9daeb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "current_affairs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("headline", sa.String(length=300), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("source_name", sa.String(length=120), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("published_date", sa.Date(), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("exam_tags", postgresql.ARRAY(sa.String(length=60)), nullable=False),
        sa.Column("importance", sa.String(length=20), nullable=False, server_default="medium"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_current_affairs_id"), "current_affairs", ["id"], unique=False)
    op.create_index(
        op.f("ix_current_affairs_published_date"),
        "current_affairs",
        ["published_date"],
        unique=False,
    )
    op.create_index(
        op.f("ix_current_affairs_category"),
        "current_affairs",
        ["category"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_current_affairs_category"), table_name="current_affairs")
    op.drop_index(op.f("ix_current_affairs_published_date"), table_name="current_affairs")
    op.drop_index(op.f("ix_current_affairs_id"), table_name="current_affairs")
    op.drop_table("current_affairs")
