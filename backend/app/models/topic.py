from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(String(500), nullable=True)

    difficulty = Column(String(20), default="Medium")

    estimated_time = Column(Integer, default=60)

    is_active = Column(Boolean, default=True)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
    )

    subject = relationship(
        "Subject",
        back_populates="topics",
    )

    questions = relationship(
        "Question",
        back_populates="topic",
        cascade="all, delete",
    )