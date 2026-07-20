from datetime import datetime

from sqlalchemy.orm import Session

from app.core.constants import (
    TEST_STATUS_IN_PROGRESS,
    TEST_STATUS_SUBMITTED,
)
from app.models.attempt_answer import AttemptAnswer
from app.models.attempt_question import AttemptQuestion
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.test_question import TestQuestion
from app.models.user import User
from app.schemas.test_attempt import (
    TestAttemptCreate,
    TestAttemptUpdate,
)
from app.services.mistake_notebook_service import add_mistake


def get_test_attempts(db: Session):
    return db.query(TestAttempt).all()


def get_test_attempt(db: Session, attempt_id: int):
    return db.query(TestAttempt).filter(TestAttempt.id == attempt_id).first()


def create_test_attempt(db: Session, user_id: int, attempt: TestAttemptCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    test = db.query(Test).filter(Test.id == attempt.test_id).first()
    if not test:
        return None

    existing = db.query(TestAttempt).filter(
        TestAttempt.user_id == user_id,
        TestAttempt.test_id == attempt.test_id,
        TestAttempt.status == TEST_STATUS_IN_PROGRESS,
    ).first()

    if existing:
        return existing

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

    test_questions = (
        db.query(TestQuestion)
        .filter(TestQuestion.test_id == attempt.test_id)
        .order_by(TestQuestion.display_order)
        .all()
    )

    for tq in test_questions:
        db.add(
            AttemptQuestion(
                attempt_id=db_attempt.id,
                question_id=tq.question_id,
                display_order=tq.display_order,
            )
        )

    db.commit()

    return db_attempt


def evaluate_attempt(db: Session, attempt_id: int):
    answers = (
        db.query(AttemptAnswer)
        .filter(AttemptAnswer.attempt_id == attempt_id)
        .all()
    )

    score = 0
    total_correct = 0
    total_wrong = 0
    total_skipped = 0

    for answer in answers:
        question = (
            db.query(Question)
            .filter(Question.id == answer.question_id)
            .first()
        )

        if not question:
            continue

        if answer.selected_option is None:
            total_skipped += 1

        elif answer.selected_option == question.correct_option:
            total_correct += 1
            score += question.marks

        else:
            total_wrong += 1
            score -= question.negative_marks

    return {
        "score": score,
        "total_correct": total_correct,
        "total_wrong": total_wrong,
        "total_skipped": total_skipped,
    }


def submit_test_attempt(db: Session, attempt_id: int):
    attempt = (
        db.query(TestAttempt)
        .filter(TestAttempt.id == attempt_id)
        .first()
    )

    if not attempt:
        return None

    result = evaluate_attempt(db, attempt_id)

    attempt.score = result["score"]
    attempt.total_correct = result["total_correct"]
    attempt.total_wrong = result["total_wrong"]
    attempt.total_skipped = result["total_skipped"]
    attempt.status = TEST_STATUS_SUBMITTED
    attempt.submitted_at = datetime.utcnow()

    # Automatically add wrong answers to Mistake Notebook
    answers = (
        db.query(AttemptAnswer)
        .filter(AttemptAnswer.attempt_id == attempt_id)
        .all()
    )

    for answer in answers:
        question = (
            db.query(Question)
            .filter(Question.id == answer.question_id)
            .first()
        )

        if not question:
            continue

        if (
            answer.selected_option is not None
            and answer.selected_option != question.correct_option
        ):
            add_mistake(
                db=db,
                user_id=attempt.user_id,
                question_id=question.id,
                attempt_id=attempt.id,
            )

    db.commit()
    db.refresh(attempt)

    return attempt


def update_test_attempt(db: Session, attempt_id: int, attempt: TestAttemptUpdate):
    db_attempt = (
        db.query(TestAttempt)
        .filter(TestAttempt.id == attempt_id)
        .first()
    )

    if not db_attempt:
        return None

    for k, v in attempt.model_dump(exclude_unset=True).items():
        setattr(db_attempt, k, v)

    db.commit()
    db.refresh(db_attempt)

    return db_attempt


def delete_test_attempt(db: Session, attempt_id: int):
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