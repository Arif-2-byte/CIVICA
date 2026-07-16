from pydantic import BaseModel


class TestQuestionBase(BaseModel):
    test_id: int
    question_id: int
    display_order: int


class TestQuestionCreate(TestQuestionBase):
    pass


class TestQuestionUpdate(BaseModel):
    display_order: int | None = None


class TestQuestionResponse(TestQuestionBase):
    id: int

    class Config:
        from_attributes = True