from pydantic import BaseModel


class ResultSummary(BaseModel):
    attempt_id: int
    user_id: int
    test_id: int

    score: float
    total_marks: float
    percentage: float

    correct: int
    wrong: int
    skipped: int

    accuracy: float
    status: str

    class Config:
        from_attributes = True