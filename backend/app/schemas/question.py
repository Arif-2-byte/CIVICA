from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    question_text: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    correct_option: Literal["A", "B", "C", "D"]

    explanation: Optional[str] = None

    difficulty: Optional[str] = "Medium"

    marks: Optional[int] = 2

    negative_marks: Optional[int] = 0

    year: Optional[int] = None

    source: Optional[str] = None

    topic_id: int


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None

    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None

    correct_option: Optional[Literal["A", "B", "C", "D"]] = None

    explanation: Optional[str] = None

    difficulty: Optional[str] = None

    marks: Optional[int] = None

    negative_marks: Optional[int] = None

    year: Optional[int] = None

    source: Optional[str] = None

    topic_id: Optional[int] = None

    is_active: Optional[bool] = None


class QuestionResponse(QuestionBase):
    id: int

    is_active: bool

    model_config = ConfigDict(from_attributes=True)
