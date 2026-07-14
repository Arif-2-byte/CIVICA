from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class AttemptQuestion(Base):
    __tablename__ = "attempt_questions"

    id = Column(Integer, primary_key=True, index=True)

    attempt_id = Column(
        Integer,
        ForeignKey("test_attempts.id"),
        nullable=False,
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
    )

    display_order = Column(
        Integer,
        nullable=False,
    )

    attempt = relationship(
        "TestAttempt",
        back_populates="attempt_questions",
    )

    question = relationship(
        "Question",
        back_populates="attempt_questions",
    )