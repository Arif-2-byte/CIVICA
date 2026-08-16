from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    test_id = Column(
        Integer,
        ForeignKey("tests.id"),
        nullable=False,
        index=True,
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )

    section_name = Column(
        String(100),
        nullable=True,
    )

    display_order = Column(
        Integer,
        nullable=False,
    )

    marks_override = Column(
        Float,
        nullable=True,
    )

    negative_marks_override = Column(
        Float,
        nullable=True,
    )

    is_mandatory = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    test = relationship(
        "Test",
        back_populates="test_questions",
    )

    question = relationship(
        "Question",
        back_populates="test_questions",
    )