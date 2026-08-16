from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session, joinedload

from app.models.exam import Exam
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.attempt_question import AttemptQuestion
from app.models.test_question import TestQuestion

from app.schemas.pagination import PaginatedResponse
from app.schemas.question import (
    QuestionCreate,
    QuestionUpdate,
)
from app.schemas.question_filter import QuestionFilter


# ==========================================================
# Validation
# ==========================================================

def validate_question(question: QuestionCreate):
    """
    Validate question before saving.
    """

    if len(question.options) < 2:
        raise ValueError(
            "A question must have at least two options."
        )

    correct_options = sum(
        1
        for option in question.options
        if option.is_correct
    )

    if question.question_type == "MCQ_SINGLE":

        if correct_options != 1:
            raise ValueError(
                "MCQ_SINGLE must have exactly one correct option."
            )

    elif question.question_type == "MCQ_MULTIPLE":

        if correct_options < 1:
            raise ValueError(
                "MCQ_MULTIPLE must have at least one correct option."
            )


# ==========================================================
# Create
# ==========================================================

def create_question(
    db: Session,
    question: QuestionCreate,
):

    validate_question(question)

    db_question = Question(
        topic_id=question.topic_id,
        question_text=question.question_text,
        explanation=question.explanation,
        hint=question.hint,
        difficulty=question.difficulty,
        question_type=question.question_type,
        exam_stage=question.exam_stage,
        marks=question.marks,
        negative_marks=question.negative_marks,
        estimated_time=question.estimated_time,
        language=question.language,
        year=question.year,
        source=question.source,
        image_url=question.image_url,
        is_pyq=question.is_pyq,
    )

    try:

        db.add(db_question)

        db.flush()

        for option in question.options:

            db_option = QuestionOption(
                question_id=db_question.id,
                option_text=option.option_text,
                image_url=option.image_url,
                display_order=option.display_order,
                is_correct=option.is_correct,
            )

            db.add(db_option)

        db.commit()

        db.refresh(db_question)

        return db_question

    except Exception:

        db.rollback()

        raise


# ==========================================================
# Get One Question
# ==========================================================

def get_question(
    db: Session,
    question_id: int,
):
    return (
        db.query(Question)
        .options(
            joinedload(Question.options)
        )
        .filter(
            Question.id == question_id
        )
        .first()
    )


# ==========================================================
# Get Questions
# ==========================================================

def get_questions(
    db: Session,
    filters: QuestionFilter,
):

    query = (
        db.query(Question)
        .options(
            joinedload(Question.options)
        )
        .join(Topic)
        .join(Subject)
        .join(Exam)
    )

    # -----------------------------
    # Search
    # -----------------------------

    if filters.search:

        search = f"%{filters.search}%"

        query = query.filter(
            or_(
                Question.question_text.ilike(search),
                Question.explanation.ilike(search),
            )
        )

    # -----------------------------
    # Filters
    # -----------------------------

    if filters.exam_id is not None:
        query = query.filter(
            Exam.id == filters.exam_id
        )

    if filters.subject_id is not None:
        query = query.filter(
            Subject.id == filters.subject_id
        )

    if filters.topic_id is not None:
        query = query.filter(
            Topic.id == filters.topic_id
        )

    if filters.difficulty:
        query = query.filter(
            Question.difficulty == filters.difficulty
        )

    if filters.language:
        query = query.filter(
            Question.language == filters.language
        )

    if filters.question_type:
        query = query.filter(
            Question.question_type == filters.question_type
        )

    if filters.is_pyq is not None:
        query = query.filter(
            Question.is_pyq == filters.is_pyq
        )

    if filters.year is not None:
        query = query.filter(
            Question.year == filters.year
        )

    # -----------------------------
    # Total Records
    # -----------------------------

    total = query.count()

    # -----------------------------
    # Sorting
    # -----------------------------

    sortable_columns = {
        "id": Question.id,
        "year": Question.year,
        "difficulty": Question.difficulty,
        "language": Question.language,
        "question_type": Question.question_type,
        "marks": Question.marks,
    }

    sort_column = sortable_columns.get(
        filters.sort_by,
        Question.id,
    )

    if filters.sort_order.lower() == "asc":
        query = query.order_by(
            asc(sort_column)
        )
    else:
        query = query.order_by(
            desc(sort_column)
        )

    # -----------------------------
    # Pagination
    # -----------------------------

    items = (
        query.offset(
            (filters.page - 1)
            * filters.page_size
        )
        .limit(filters.page_size)
        .all()
    )

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=filters.page,
        page_size=filters.page_size,
    )


# ==========================================================
# Update Question
# ==========================================================

def update_question(
    db: Session,
    question_id: int,
    question: QuestionUpdate,
):

    db_question = (
        db.query(Question)
        .options(
            joinedload(Question.options)
        )
        .filter(
            Question.id == question_id
        )
        .first()
    )

    if db_question is None:
        return None

    update_data = question.model_dump(
        exclude_unset=True,
        exclude={"options"},
    )

    for key, value in update_data.items():
        setattr(
            db_question,
            key,
            value,
        )

    if (
        hasattr(question, "options")
        and question.options is not None
    ):

        db.query(QuestionOption).filter(
            QuestionOption.question_id
            == db_question.id
        ).delete()

        for option in question.options:

            db.add(
                QuestionOption(
                    question_id=db_question.id,
                    option_text=option.option_text,
                    image_url=option.image_url,
                    display_order=option.display_order,
                    is_correct=option.is_correct,
                )
            )

    db.commit()
    db.refresh(db_question)

    return db_question


# ==========================================================
# Delete Question
# ==========================================================

def delete_question(
    db: Session,
    question_id: int,
):

    db_question = (
        db.query(Question)
        .filter(
            Question.id == question_id
        )
        .first()
    )

    if db_question is None:
        return None

    # ------------------------------------------------------
    # Do not delete a question that has already been used
    # in a student attempt.
    # ------------------------------------------------------

    existing_attempt_question = (
        db.query(AttemptQuestion)
        .filter(
            AttemptQuestion.question_id
            == question_id
        )
        .first()
    )

    if existing_attempt_question is not None:
        return "USED_IN_ATTEMPT"

    # ------------------------------------------------------
    # Also prevent deleting a question that is currently
    # assigned to a test.
    # ------------------------------------------------------

    existing_test_question = (
        db.query(TestQuestion)
        .filter(
            TestQuestion.question_id
            == question_id
        )
        .first()
    )

    if existing_test_question is not None:
        return "ASSIGNED_TO_TEST"

    # ------------------------------------------------------
    # Safe to delete.
    # ------------------------------------------------------

    db.delete(db_question)
    db.commit()

    return True


# ==========================================================
# Helpers
# ==========================================================

def topic_exists(
    db: Session,
    topic_id: int,
):

    return (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
        is not None
    )