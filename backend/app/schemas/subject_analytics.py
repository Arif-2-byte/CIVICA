from pydantic import BaseModel


class SubjectAnalytics(BaseModel):
    subject: str

    total_questions: int

    correct: int

    wrong: int

    skipped: int

    marks: float

    accuracy: float

    class Config:
        from_attributes = True