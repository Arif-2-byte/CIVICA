from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    description = Column(String(500), nullable=True)

    total_questions = Column(Integer, nullable=False)

    duration = Column(Integer, nullable=False)

    total_marks = Column(Integer, nullable=False)

    negative_marks = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

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
)
    
    test_questions = relationship(
    "TestQuestion",
    back_populates="test",
    cascade="all, delete",
)   