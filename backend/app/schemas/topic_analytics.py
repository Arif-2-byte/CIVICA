from pydantic import BaseModel


class TopicAnalytics(BaseModel):
    topic: str

    subject: str

    total_questions: int

    correct: int

    wrong: int

    skipped: int

    marks: float

    accuracy: float

    class Config:
        from_attributes = True