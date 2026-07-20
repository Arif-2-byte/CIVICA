from datetime import datetime
from typing import List

from pydantic import BaseModel


class RecentTest(BaseModel):
    attempt_id: int
    test_name: str
    score: int
    status: str
    submitted_at: datetime | None

    class Config:
        from_attributes = True


class Dashboard(BaseModel):
    tests_attempted: int
    tests_completed: int

    average_score: float
    highest_score: int

    average_accuracy: float

    total_correct: int
    total_wrong: int
    total_skipped: int

    recent_tests: List[RecentTest]

    class Config:
        from_attributes = True