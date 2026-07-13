from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .models import Category, Importance


class CurrentAffairBase(BaseModel):
    headline: str = Field(..., max_length=300)
    summary: str
    source_name: str
    source_url: Optional[str] = None
    published_date: date
    category: Category
    exam_tags: List[str] = []
    importance: Importance = Importance.MEDIUM


class CurrentAffairCreate(CurrentAffairBase):
    pass


class CurrentAffairOut(CurrentAffairBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedCurrentAffairs(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[CurrentAffairOut]
