from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    question_text = Column(Text, nullable=False)

    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False)
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)

    correct_option = Column(String(1), nullable=False)

    explanation = Column(Text, nullable=True)

    difficulty = Column(String(20), nullable=True)

    marks = Column(Integer, default=2)

    negative_marks = Column(Integer, default=0)

    year = Column(Integer, nullable=True)

    source = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True)

    topic_id = Column(
        Integer,
        ForeignKey("topics.id"),
        nullable=False,
    )

    topic = relationship(
        "Topic",
        back_populates="questions",
    )

    attempt_questions = relationship(
        "AttemptQuestion",
        back_populates="question",
        cascade="all, delete",
    )
    