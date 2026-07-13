import enum

from sqlalchemy import Column, Date, Enum as SqlEnum, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base


class Category(str, enum.Enum):
    POLITY_GOVERNANCE = "Polity & Governance"
    ECONOMY = "Economy"
    ENVIRONMENT_ECOLOGY = "Environment & Ecology"
    SCIENCE_TECH = "Science & Technology"
    INTERNATIONAL_RELATIONS = "International Relations"
    AWARDS_HONOURS = "Awards & Honours"
    SPORTS = "Sports"
    DEFENCE_SECURITY = "Defence & Security"
    PERSON_IN_NEWS = "Person in News"
    PLACE_IN_NEWS = "Place in News"
    SCHEMES_POLICIES = "Schemes & Policies"
    REPORTS_INDICES = "Reports & Indices"


class Importance(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CurrentAffair(Base):
    __tablename__ = "current_affairs"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String(300), nullable=False)
    summary = Column(Text, nullable=False)
    source_name = Column(String(120), nullable=False)
    source_url = Column(String(500), nullable=True)
    published_date = Column(Date, nullable=False, index=True)
    category = Column(SqlEnum(Category, name="category_enum"), nullable=False, index=True)
    exam_tags = Column(ARRAY(String), nullable=False, default=list)
    importance = Column(
        SqlEnum(Importance, name="importance_enum"), nullable=False, default=Importance.MEDIUM
    )
