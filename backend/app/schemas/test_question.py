from pydantic import BaseModel, ConfigDict, Field


class TestQuestionBase(BaseModel):
    test_id: int
    question_id: int

    section_name: str | None = None

    display_order: int = Field(..., ge=1)

    marks_override: float | None = Field(
        default=None,
        ge=0,
    )

    negative_marks_override: float | None = Field(
        default=None,
        ge=0,
    )

    is_mandatory: bool = False


class TestQuestionCreate(TestQuestionBase):
    pass


class TestQuestionUpdate(BaseModel):
    section_name: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=1,
    )

    marks_override: float | None = Field(
        default=None,
        ge=0,
    )

    negative_marks_override: float | None = Field(
        default=None,
        ge=0,
    )

    is_mandatory: bool | None = None


class TestQuestionResponse(TestQuestionBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )