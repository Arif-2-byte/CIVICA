from pydantic import BaseModel, ConfigDict


class AttemptAnswerBase(BaseModel):
    attempt_id: int
    question_id: int
    selected_option: int | None = None
    is_marked_for_review: bool = False


class AttemptAnswerCreate(AttemptAnswerBase):
    pass


class AttemptAnswerUpdate(BaseModel):
    selected_option: int | None = None
    is_marked_for_review: bool | None = None


class AttemptAnswerResponse(AttemptAnswerBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )