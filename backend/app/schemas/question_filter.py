from typing import Optional

from pydantic import BaseModel


class QuestionFilter(BaseModel):
    page: int = 1
    page_size: int = 20

    search: Optional[str] = None

    exam_id: Optional[int] = None
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None

    difficulty: Optional[str] = None

    language: Optional[str] = None

    question_type: Optional[str] = None

    is_pyq: Optional[bool] = None

    year: Optional[int] = None

    sort_by: str = "id"

    sort_order: str = "desc"