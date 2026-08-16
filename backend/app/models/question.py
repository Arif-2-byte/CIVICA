from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.core.enums import (
    DifficultyLevel,
    QuestionType,
    ExamStage,
)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    question_text = Column(
        Text,
        nullable=False,
    )

    explanation = Column(
        Text,
        nullable=True,
    )

    hint = Column(
        Text,
        nullable=True,
    )

    # Keep these as String columns in the database.
    # We still use the enums for the default values.
    difficulty = Column(
        String(20),
        nullable=False,
        default=DifficultyLevel.MEDIUM.value,
    )

    question_type = Column(
        String(30),
        nullable=False,
        default=QuestionType.MCQ_SINGLE.value,
    )

    exam_stage = Column(
        String(30),
        nullable=False,
        default=ExamStage.PRELIMS.value,
    )

    marks = Column(
        Float,
        nullable=False,
        default=2.0,
    )

    negative_marks = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    estimated_time = Column(
        Integer,
        nullable=False,
        default=60,
    )

    language = Column(
        String(20),
        nullable=False,
        default="English",
    )

    year = Column(
        Integer,
        nullable=True,
    )

    source = Column(
        String(100),
        nullable=True,
    )

    image_url = Column(
        String(500),
        nullable=True,
    )

    is_pyq = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    topic_id = Column(
        Integer,
        ForeignKey("topics.id"),
        nullable=False,
        index=True,
    )

    topic = relationship(
        "Topic",
        back_populates="questions",
    )

    options = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete-orphan",
    )

    attempt_questions = relationship(
        "AttemptQuestion",
        back_populates="question",
    )

    attempt_answers = relationship(
        "AttemptAnswer",
        back_populates="question",
    )

    test_questions = relationship(
        "TestQuestion",
        back_populates="question",
        cascade="all, delete-orphan",
    )

    mistake_notebook_entries = relationship(
        "MistakeNotebook",
        back_populates="question",
        cascade="all, delete-orphan",
    )