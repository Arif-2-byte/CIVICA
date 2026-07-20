from datetime import datetime

from pydantic import BaseModel


class MistakeNotebookBase(BaseModel):
    question_id: int
    attempt_id: int


class MistakeNotebookCreate(MistakeNotebookBase):
    pass


class MistakeNotebookResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    attempt_id: int
    revision_count: int
    mastered: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class MistakeQuestionResponse(BaseModel):
    id: int
    question_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    explanation: str | None
    revision_count: int
    mastered: bool

    model_config = {
        "from_attributes": True
    }