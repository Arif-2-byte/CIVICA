from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.attempt_question import AttemptQuestion
from app.schemas.test_question import (
    TestQuestionCreate,
    TestQuestionUpdate,
)


def get_test_questions(
    db: Session,
    test_id: int | None = None,
):
    query = db.query(TestQuestion)

    if test_id is not None:
        query = query.filter(
            TestQuestion.test_id == test_id
        )

    return (
        query
        .order_by(TestQuestion.display_order)
        .all()
    )


def get_test_question(
    db: Session,
    test_question_id: int,
):
    return (
        db.query(TestQuestion)
        .filter(
            TestQuestion.id == test_question_id
        )
        .first()
    )


def create_test_question(
    db: Session,
    test_question: TestQuestionCreate,
):
    # Check if test exists
    test = (
        db.query(Test)
        .filter(
            Test.id == test_question.test_id
        )
        .first()
    )

    if test is None:
        return None

    # Check if question exists
    question = (
        db.query(Question)
        .filter(
            Question.id == test_question.question_id
        )
        .first()
    )

    if question is None:
        return None

    # Do not allow inactive questions
    if not question.is_active:
        return None

    # Prevent duplicate question in same test
    existing = (
        db.query(TestQuestion)
        .filter(
            TestQuestion.test_id
            == test_question.test_id,
            TestQuestion.question_id
            == test_question.question_id,
        )
        .first()
    )

    if existing is not None:
        return existing

    # Create test-question mapping
    db_test_question = TestQuestion(
        **test_question.model_dump()
    )

    db.add(db_test_question)
    db.commit()
    db.refresh(db_test_question)

    return db_test_question


def update_test_question(
    db: Session,
    test_question_id: int,
    test_question: TestQuestionUpdate,
):
    db_test_question = get_test_question(
        db,
        test_question_id,
    )

    if db_test_question is None:
        return None

    update_data = test_question.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_test_question,
            key,
            value,
        )

    db.commit()
    db.refresh(db_test_question)

    return db_test_question


def delete_test_question(
    db: Session,
    test_question_id: int,
):
    db_test_question = get_test_question(
        db,
        test_question_id,
    )

    if db_test_question is None:
        return None

    # ------------------------------------------------------
    # IMPORTANT:
    # Do not delete a test-question mapping if this question
    # has already been used in a student attempt.
    # ------------------------------------------------------

    existing_attempt_question = (
        db.query(AttemptQuestion)
        .filter(
            AttemptQuestion.question_id
            == db_test_question.question_id
        )
        .first()
    )

    if existing_attempt_question is not None:
        return "USED_IN_ATTEMPT"

    db.delete(db_test_question)
    db.commit()

    return True