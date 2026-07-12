from pydantic import BaseModel


class ExamResponse(BaseModel):
    id: int
    name: str
    short_name: str
    description: str | None
    icon: str | None
    is_active: bool

    class Config:
        from_attributes = True