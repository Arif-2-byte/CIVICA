from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionOption(BaseModel):
    id: int
    option_text: str


class SessionQuestion(BaseModel):
    attempt_question_id: int
    question_id: int
    display_order: int
    question_text: str
    marks: float
    negative_marks: float
    options: list[SessionOption]
    selected_option: int | None = None
    is_marked_for_review: bool = False


class TestSessionResponse(BaseModel):
    attempt_id: int
    test_id: int
    title: str
    description: str | None = None
    duration: int | None = None
    total_questions: int
    total_marks: float
    status: str
    started_at: datetime
    questions: list[SessionQuestion]

    model_config = ConfigDict(
        from_attributes=True
    )