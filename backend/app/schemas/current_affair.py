from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class CurrentAffairBase(BaseModel):
    headline: str = Field(max_length=300)
    summary: str
    source_name: str = Field(max_length=120)
    source_url: str | None = Field(default=None, max_length=500)
    published_date: date
    category: str = Field(max_length=80)
    exam_tags: list[str] = Field(default_factory=list)
    importance: str = Field(default="medium", pattern="^(high|medium|low)$")


class CurrentAffairCreate(CurrentAffairBase):
    pass


class CurrentAffairResponse(CurrentAffairBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CurrentAffairPage(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[CurrentAffairResponse]
