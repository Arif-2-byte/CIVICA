from pydantic import BaseModel, ConfigDict


class AnswerReview(BaseModel):
    question_id: int

    question: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    your_answer: int | None

    correct_answer: int

    is_correct: bool

    marks_awarded: float

    explanation: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )