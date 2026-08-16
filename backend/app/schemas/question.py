from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import (
    DifficultyLevel,
    QuestionType,
    ExamStage,
)


# ==========================================================
# Question Options
# ==========================================================

class QuestionOptionCreate(BaseModel):
    option_text: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )

    image_url: Optional[str] = None

    display_order: int = Field(
        ...,
        ge=1,
    )

    is_correct: bool = False


class QuestionOptionResponse(BaseModel):
    id: int

    option_text: str

    image_url: Optional[str] = None

    display_order: int

    is_correct: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
    # ==========================================================
# Create
# ==========================================================

class QuestionCreate(BaseModel):
    topic_id: int

    question_text: str = Field(
        ...,
        min_length=5,
    )

    explanation: Optional[str] = None

    hint: Optional[str] = None

    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM

    question_type: QuestionType = QuestionType.MCQ_SINGLE

    exam_stage: ExamStage = ExamStage.PRELIMS

    marks: float = 2.0

    negative_marks: float = 0.0

    estimated_time: int = 60

    language: str = "English"

    year: Optional[int] = None

    source: Optional[str] = None

    image_url: Optional[str] = None

    is_pyq: bool = False

    options: list[QuestionOptionCreate]


# ==========================================================
# Update
# ==========================================================

class QuestionUpdate(BaseModel):
    topic_id: Optional[int] = None

    question_text: Optional[str] = None

    explanation: Optional[str] = None

    hint: Optional[str] = None

    difficulty: Optional[DifficultyLevel] = None

    question_type: Optional[QuestionType] = None

    exam_stage: Optional[ExamStage] = None

    marks: Optional[float] = None

    negative_marks: Optional[float] = None

    estimated_time: Optional[int] = None

    language: Optional[str] = None

    year: Optional[int] = None

    source: Optional[str] = None

    image_url: Optional[str] = None

    is_pyq: Optional[bool] = None

    is_active: Optional[bool] = None

    options: Optional[list[QuestionOptionCreate]] = None
    # ==========================================================
# Response
# ==========================================================

class QuestionResponse(BaseModel):
    id: int

    topic_id: int

    question_text: str

    explanation: Optional[str] = None

    hint: Optional[str] = None

    difficulty: DifficultyLevel

    question_type: QuestionType

    exam_stage: ExamStage

    marks: float

    negative_marks: float

    estimated_time: int

    language: str

    year: Optional[int] = None

    source: Optional[str] = None

    image_url: Optional[str] = None

    is_pyq: bool

    is_active: bool

    options: list[QuestionOptionResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )