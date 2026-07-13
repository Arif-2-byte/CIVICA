from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TestAttemptBase(BaseModel):
    test_id: int


class TestAttemptCreate(TestAttemptBase):
    pass


class TestAttemptUpdate(BaseModel):
    score: Optional[int] = None
    total_correct: Optional[int] = None
    total_wrong: Optional[int] = None
    total_skipped: Optional[int] = None
    status: Optional[str] = None
    submitted_at: Optional[datetime] = None


class TestAttemptResponse(BaseModel):
    id: int
    user_id: int
    test_id: int
    score: int
    total_correct: int
    total_wrong: int
    total_skipped: int
    status: str
    started_at: datetime
    submitted_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }