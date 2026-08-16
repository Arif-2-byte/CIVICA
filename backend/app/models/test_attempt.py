from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    test_id = Column(
        Integer,
        ForeignKey("tests.id"),
        nullable=False,
        index=True,
    )

    score = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    total_correct = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_wrong = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_skipped = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        String(20),
        nullable=False,
        default="In Progress",
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    submitted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="test_attempts",
    )

    test = relationship(
        "Test",
        back_populates="attempts",
    )

    attempt_questions = relationship(
        "AttemptQuestion",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )

    attempt_answers = relationship(
        "AttemptAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )

    mistake_notebook_entries = relationship(
        "MistakeNotebook",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )