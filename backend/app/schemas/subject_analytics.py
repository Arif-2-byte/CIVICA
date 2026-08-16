from pydantic import BaseModel, ConfigDict


class SubjectAnalytics(BaseModel):
    subject: str

    total_questions: int

    correct: int

    wrong: int

    skipped: int

    marks: float

    accuracy: float

    model_config = ConfigDict(
        from_attributes=True
    )