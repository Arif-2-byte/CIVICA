from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    test_id = Column(
        Integer,
        ForeignKey("tests.id"),
        nullable=False,
    )

    score = Column(Integer, default=0)

    total_correct = Column(Integer, default=0)

    total_wrong = Column(Integer, default=0)

    total_skipped = Column(Integer, default=0)

    status = Column(
        String(20),
        default="In Progress",
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
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
    )

    attempt_answers = relationship(
        "AttemptAnswer",
        back_populates="attempt",
        cascade="all, delete",
    )

    mistake_notebook_entries = relationship(
    "MistakeNotebook",
    back_populates="attempt",
    cascade="all, delete-orphan",
)