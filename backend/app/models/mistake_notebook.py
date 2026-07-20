from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class MistakeNotebook(Base):
    __tablename__ = "mistake_notebook"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
    )

    attempt_id = Column(
        Integer,
        ForeignKey("test_attempts.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    revision_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    mastered = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="mistake_notebook",
    )

    question = relationship(
        "Question",
        back_populates="mistake_notebook_entries",
    )

    attempt = relationship(
        "TestAttempt",
        back_populates="mistake_notebook_entries",
    )