from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(String(500), nullable=True)

    exam_id = Column(
        Integer,
        ForeignKey("exams.id"),
        nullable=False,
    )

    exam = relationship(
        "Exam",
        back_populates="subjects",
    )

    topics = relationship(
        "Topic",
        back_populates="subject",
        cascade="all, delete",
    )
