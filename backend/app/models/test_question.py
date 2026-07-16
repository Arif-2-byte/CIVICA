from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("tests.id"),
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

    test = relationship(
        "Test",
        back_populates="test_questions",
    )

    question = relationship(
        "Question",
        back_populates="test_questions",
    )