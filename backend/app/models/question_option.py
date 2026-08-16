from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )

    option_text = Column(
        String(500),
        nullable=False,
    )

    image_url = Column(
        String(500),
        nullable=True,
    )

    display_order = Column(
        Integer,
        nullable=False,
    )

    is_correct = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    question = relationship(
        "Question",
        back_populates="options",
    )