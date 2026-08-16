from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.database import Base


class CurrentAffair(Base):
    __tablename__ = "current_affairs"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String(300), nullable=False)
    summary = Column(Text, nullable=False)
    source_name = Column(String(120), nullable=False)
    source_url = Column(String(500), nullable=True)
    published_date = Column(Date, nullable=False, index=True)
    category = Column(String(80), nullable=False, index=True)
    exam_tags = Column(ARRAY(String(60)), nullable=False, default=list)
    importance = Column(String(20), nullable=False, default="medium")
