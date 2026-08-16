from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecentTest(BaseModel):
    attempt_id: int
    test_name: str
    score: float
    status: str
    submitted_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class Dashboard(BaseModel):
    tests_attempted: int
    tests_completed: int

    average_score: float
    highest_score: float

    average_accuracy: float

    total_correct: int
    total_wrong: int
    total_skipped: int

    recent_tests: list[RecentTest]

    model_config = ConfigDict(
        from_attributes=True
    )