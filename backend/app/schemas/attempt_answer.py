from pydantic import BaseModel


class AttemptAnswerBase(BaseModel):
    attempt_id: int
    question_id: int
    selected_option: str | None = None
    is_marked_for_review: bool = False


class AttemptAnswerCreate(AttemptAnswerBase):
    pass


class AttemptAnswerUpdate(BaseModel):
    selected_option: str | None = None
    is_marked_for_review: bool | None = None


class AttemptAnswerResponse(AttemptAnswerBase):
    id: int

    class Config:
        from_attributes = True