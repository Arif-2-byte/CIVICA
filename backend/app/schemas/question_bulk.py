from typing import List

from pydantic import BaseModel, Field


class BulkQuestionRequest(BaseModel):
    question_ids: List[int] = Field(
        ...,
        min_length=1,
        description="List of Question IDs",
    )


class BulkOperationResponse(BaseModel):
    message: str
    affected_rows: int