from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    instructions = Column(
        Text,
        nullable=True,
    )

    test_type = Column(
        String(30),
        nullable=False,
        default="Mock Test",
    )

    difficulty = Column(
        String(20),
        nullable=False,
        default="Mixed",
    )

    language = Column(
        String(30),
        nullable=False,
        default="English",
    )

    total_questions = Column(
        Integer,
        nullable=False,
    )

    duration = Column(
        Integer,
        nullable=False,
    )

    total_marks = Column(
        Float,
        nullable=False,
    )

    passing_marks = Column(
        Float,
        nullable=False,
        default=0,
    )

    negative_marks = Column(
        Float,
        nullable=False,
        default=0,
    )

    shuffle_questions = Column(
        Boolean,
        default=False,
    )

    shuffle_options = Column(
        Boolean,
        default=False,
    )

    show_result = Column(
        Boolean,
        default=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    is_published = Column(
        Boolean,
        default=False,
    )

    start_time = Column(
        DateTime,
        nullable=True,
    )

    end_time = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    exam_id = Column(
        Integer,
        ForeignKey("exams.id"),
        nullable=False,
    )

    exam = relationship(
        "Exam",
        back_populates="tests",
    )

    attempts = relationship(
        "TestAttempt",
        back_populates="test",
        cascade="all, delete-orphan",
    )

    test_questions = relationship(
        "TestQuestion",
        back_populates="test",
        cascade="all, delete-orphan",
    )