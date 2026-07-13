from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    short_name = Column(String(30), unique=True, nullable=False)

    description = Column(String(500))

    icon = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    subjects = relationship(
    "Subject",
    back_populates="exam",
    cascade="all, delete",
)