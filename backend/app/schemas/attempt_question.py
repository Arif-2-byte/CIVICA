from pydantic import BaseModel


class AttemptQuestionBase(BaseModel):
    attempt_id: int
    question_id: int
    display_order: int


class AttemptQuestionCreate(AttemptQuestionBase):
    pass


class AttemptQuestionResponse(AttemptQuestionBase):
    id: int

    model_config = {
        "from_attributes": True
    }