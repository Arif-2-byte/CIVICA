from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.constants import (
    TEST_STATUS_IN_PROGRESS,
    TEST_STATUS_SUBMITTED,
)
from app.models.attempt_answer import AttemptAnswer
from app.models.attempt_question import AttemptQuestion
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.test_question import TestQuestion
from app.models.user import User
from app.schemas.test_attempt import (
    TestAttemptCreate,
    TestAttemptUpdate,
)
from app.services.mistake_notebook_service import add_mistake


def get_test_attempts(
    db: Session,
):
    return (
        db.query(TestAttempt)
        .order_by(TestAttempt.id.desc())
        .all()
    )


def get_test_attempt(
    db: Session,
    attempt_id: int,
):
    return (
        db.query(TestAttempt)
        .filter(
            TestAttempt.id == attempt_id
        )
        .first()
    )


def get_user_attempts(
    db: Session,
    user_id: int,
):
    return (
        db.query(TestAttempt)
        .filter(
            TestAttempt.user_id == user_id
        )
        .order_by(TestAttempt.id.desc())
        .all()
    )


def create_test_attempt(
    db: Session,
    user_id: int,
    attempt: TestAttemptCreate,
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        return None

    test = (
        db.query(Test)
        .filter(Test.id == attempt.test_id)
        .first()
    )

    if test is None:
        return None

    # Prevent multiple active attempts
    existing = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.user_id == user_id,
            TestAttempt.test_id == attempt.test_id,
            TestAttempt.status
            == TEST_STATUS_IN_PROGRESS,
        )
        .first()
    )

    if existing is not None:
        return existing

    db_attempt = TestAttempt(
        user_id=user_id,
        test_id=attempt.test_id,
        score=0.0,
        total_correct=0,
        total_wrong=0,
        total_skipped=0,
        status=TEST_STATUS_IN_PROGRESS,
    )

    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)

    # Get questions assigned to this test
    test_questions = (
        db.query(TestQuestion)
        .filter(
            TestQuestion.test_id == attempt.test_id
        )
        .order_by(
            TestQuestion.display_order
        )
        .all()
    )

    # Create snapshot of questions for this attempt
    for test_question in test_questions:
        db.add(
            AttemptQuestion(
                attempt_id=db_attempt.id,
                question_id=test_question.question_id,
                display_order=test_question.display_order,
            )
        )

    db.commit()

    return db_attempt


def evaluate_attempt(
    db: Session,
    attempt_id: int,
):
    # Get every question assigned to this attempt
    attempt_questions = (
        db.query(AttemptQuestion)
        .filter(
            AttemptQuestion.attempt_id == attempt_id
        )
        .all()
    )

    # Get all submitted answers for this attempt
    answers = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.attempt_id == attempt_id
        )
        .all()
    )

    # Make lookup:
    # question_id -> answer
    answer_map = {
        answer.question_id: answer
        for answer in answers
    }

    score = 0.0
    total_correct = 0
    total_wrong = 0
    total_skipped = 0

    # Evaluate every question in the attempt
    for attempt_question in attempt_questions:

        question = (
            db.query(Question)
            .filter(
                Question.id
                == attempt_question.question_id
            )
            .first()
        )

        if question is None:
            continue

        # Check whether the question was answered
        answer = answer_map.get(
            attempt_question.question_id
        )

        # No answer record = skipped
        if answer is None:
            total_skipped += 1
            continue

        # Answer record exists but no option selected
        if answer.selected_option is None:
            total_skipped += 1
            continue

        # Find selected option
        selected_option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.id
                == answer.selected_option,
                QuestionOption.question_id
                == question.id,
            )
            .first()
        )

        # Invalid option
        if selected_option is None:
            total_wrong += 1
            score -= question.negative_marks
            continue

        # Correct answer
        if selected_option.is_correct:
            total_correct += 1
            score += question.marks

        # Wrong answer
        else:
            total_wrong += 1
            score -= question.negative_marks

    return {
        "score": score,
        "total_correct": total_correct,
        "total_wrong": total_wrong,
        "total_skipped": total_skipped,
    }

def submit_test_attempt(
    db: Session,
    attempt_id: int,
):
    attempt = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.id == attempt_id
        )
        .first()
    )

    if attempt is None:
        return None

    # Don't submit an already submitted attempt
    if attempt.status == TEST_STATUS_SUBMITTED:
        return attempt

    result = evaluate_attempt(
        db,
        attempt_id,
    )

    attempt.score = result["score"]
    attempt.total_correct = result["total_correct"]
    attempt.total_wrong = result["total_wrong"]
    attempt.total_skipped = result["total_skipped"]

    attempt.status = TEST_STATUS_SUBMITTED

    attempt.submitted_at = datetime.now(
        timezone.utc
    )

    # Add wrong answers to Mistake Notebook
    answers = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.attempt_id == attempt_id
        )
        .all()
    )

    for answer in answers:

        if answer.selected_option is None:
            continue

        question = (
            db.query(Question)
            .filter(
                Question.id == answer.question_id
            )
            .first()
        )

        if question is None:
            continue

        selected_option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.id
                == answer.selected_option,
                QuestionOption.question_id
                == question.id,
            )
            .first()
        )

        if (
            selected_option is not None
            and not selected_option.is_correct
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


def update_test_attempt(
    db: Session,
    attempt_id: int,
    attempt: TestAttemptUpdate,
):
    db_attempt = get_test_attempt(
        db,
        attempt_id,
    )

    if db_attempt is None:
        return None

    update_data = attempt.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_attempt,
            key,
            value,
        )

    db.commit()
    db.refresh(db_attempt)

    return db_attempt


def delete_test_attempt(
    db: Session,
    attempt_id: int,
):
    db_attempt = get_test_attempt(
        db,
        attempt_id,
    )

    if db_attempt is None:
        return False

    db.delete(db_attempt)
    db.commit()

    return True