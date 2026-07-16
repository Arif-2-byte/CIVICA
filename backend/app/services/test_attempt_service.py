from sqlalchemy.orm import Session

from app.core.constants import TEST_STATUS_IN_PROGRESS
from app.models.attempt_question import AttemptQuestion
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.test_question import TestQuestion
from app.models.user import User
from app.schemas.test_attempt import (
    TestAttemptCreate,
    TestAttemptUpdate,
)


def get_test_attempts(db: Session):
    return db.query(TestAttempt).all()


def get_test_attempt(db: Session, attempt_id: int):
    return (
        db.query(TestAttempt)
        .filter(TestAttempt.id == attempt_id)
        .first()
    )


def create_test_attempt(
    db: Session,
    user_id: int,
    attempt: TestAttemptCreate,
):
    # Check if user exists
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    # Check if test exists
    test = (
        db.query(Test)
        .filter(Test.id == attempt.test_id)
        .first()
    )

    if not test:
        return None

    # Check if an active attempt already exists
    existing_attempt = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.user_id == user_id,
            TestAttempt.test_id == attempt.test_id,
            TestAttempt.status == TEST_STATUS_IN_PROGRESS,
        )
        .first()
    )

    if existing_attempt:
        return existing_attempt

    # Create new test attempt
    db_attempt = TestAttempt(
        user_id=user_id,
        test_id=attempt.test_id,
        score=0,
        total_correct=0,
        total_wrong=0,
        total_skipped=0,
        status=TEST_STATUS_IN_PROGRESS,
    )

    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)

    # Fetch all questions assigned to this test
    test_questions = (
        db.query(TestQuestion)
        .filter(TestQuestion.test_id == attempt.test_id)
        .order_by(TestQuestion.display_order)
        .all()
    )

    # Create AttemptQuestion entries
    for test_question in test_questions:

        attempt_question = AttemptQuestion(
            attempt_id=db_attempt.id,
            question_id=test_question.question_id,
            display_order=test_question.display_order,
        )

        db.add(attempt_question)

    db.commit()

    return db_attempt


def update_test_attempt(
    db: Session,
    attempt_id: int,
    attempt: TestAttemptUpdate,
):
    db_attempt = (
        db.query(TestAttempt)
        .filter(TestAttempt.id == attempt_id)
        .first()
    )

    if not db_attempt:
        return None

    update_data = attempt.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_attempt, key, value)

    db.commit()
    db.refresh(db_attempt)

    return db_attempt


def delete_test_attempt(
    db: Session,
    attempt_id: int,
):
    db_attempt = (
        db.query(TestAttempt)
        .filter(TestAttempt.id == attempt_id)
        .first()
    )

    if not db_attempt:
        return False

    db.delete(db_attempt)
    db.commit()

    return True