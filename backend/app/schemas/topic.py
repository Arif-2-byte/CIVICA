from pydantic import BaseModel


class TopicCreate(BaseModel):
    name: str
    description: str | None = None
    difficulty: str = "Medium"
    estimated_time: int = 60
    subject_id: int


class TopicResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    difficulty: str
    estimated_time: int
    is_active: bool
    subject_id: int

    class Config:
        from_attributes = True