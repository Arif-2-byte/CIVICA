from typing import Optional

from pydantic import BaseModel


class TestBase(BaseModel):
    title: str
    description: Optional[str] = None
    total_questions: int
    duration: int
    total_marks: int
    negative_marks: int = 0
    is_active: bool = True
    exam_id: int


class TestCreate(TestBase):
    pass


class TestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    total_questions: Optional[int] = None
    duration: Optional[int] = None
    total_marks: Optional[int] = None
    negative_marks: Optional[int] = None
    is_active: Optional[bool] = None
    exam_id: Optional[int] = None


class TestResponse(TestBase):
    id: int

    class Config:
        from_attributes = True