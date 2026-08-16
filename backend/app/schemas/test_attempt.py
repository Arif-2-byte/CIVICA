from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TestAttemptBase(BaseModel):
    test_id: int


class TestAttemptCreate(TestAttemptBase):
    pass


class TestAttemptUpdate(BaseModel):
    score: Optional[float] = Field(
        default=None,
        ge=0,
    )

    total_correct: Optional[int] = Field(
        default=None,
        ge=0,
    )

    total_wrong: Optional[int] = Field(
        default=None,
        ge=0,
    )

    total_skipped: Optional[int] = Field(
        default=None,
        ge=0,
    )

    status: Optional[str] = None

    submitted_at: Optional[datetime] = None


class TestAttemptResponse(BaseModel):
    id: int

    user_id: int

    test_id: int

    score: float

    total_correct: int

    total_wrong: int

    total_skipped: int

    status: str

    started_at: datetime

    submitted_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
    )