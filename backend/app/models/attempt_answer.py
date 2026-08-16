from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    attempt_id = Column(
        Integer,
        ForeignKey("test_attempts.id"),
        nullable=False,
        index=True,
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )

    # Stores question_options.id
    selected_option = Column(
        Integer,
        nullable=True,
    )

    is_marked_for_review = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    answered_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    attempt = relationship(
        "TestAttempt",
        back_populates="attempt_answers",
    )

    question = relationship(
        "Question",
        back_populates="attempt_answers",
    )