from pydantic import BaseModel


class AnswerReview(BaseModel):
    question_id: int

    question: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    your_answer: str | None

    correct_answer: str

    is_correct: bool

    marks_awarded: float

    explanation: str | None

    class Config:
        from_attributes = True