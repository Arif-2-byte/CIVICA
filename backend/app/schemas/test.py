from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TestBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)

    description: Optional[str] = None

    instructions: Optional[str] = None

    test_type: str = "Mock Test"

    difficulty: str = "Mixed"

    language: str = "English"

    total_questions: int = Field(..., gt=0)

    duration: int = Field(..., gt=0)

    total_marks: float = Field(..., gt=0)

    passing_marks: float = 0

    negative_marks: float = 0

    shuffle_questions: bool = False

    shuffle_options: bool = False

    show_result: bool = True

    is_active: bool = True

    is_published: bool = False

    start_time: Optional[datetime] = None

    end_time: Optional[datetime] = None

    exam_id: int


class TestCreate(TestBase):
    pass


class TestUpdate(BaseModel):
    title: Optional[str] = None

    description: Optional[str] = None

    instructions: Optional[str] = None

    test_type: Optional[str] = None

    difficulty: Optional[str] = None

    language: Optional[str] = None

    total_questions: Optional[int] = None

    duration: Optional[int] = None

    total_marks: Optional[float] = None

    passing_marks: Optional[float] = None

    negative_marks: Optional[float] = None

    shuffle_questions: Optional[bool] = None

    shuffle_options: Optional[bool] = None

    show_result: Optional[bool] = None

    is_active: Optional[bool] = None

    is_published: Optional[bool] = None

    start_time: Optional[datetime] = None

    end_time: Optional[datetime] = None

    exam_id: Optional[int] = None


class TestResponse(TestBase):
    id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )