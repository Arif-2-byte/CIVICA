from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.models.question import Question
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.test_attempt import TestAttempt
from app.schemas.test import TestCreate, TestUpdate


def exam_exists(
    db: Session,
    exam_id: int,
):
    return (
        db.query(Exam)
        .filter(Exam.id == exam_id)
        .first()
        is not None
    )


def get_tests(
    db: Session,
):
    return (
        db.query(Test)
        .order_by(desc(Test.id))
        .all()
    )


def get_test(
    db: Session,
    test_id: int,
):
    return (
        db.query(Test)
        .filter(Test.id == test_id)
        .first()
    )


def create_test(
    db: Session,
    test: TestCreate,
):
    if not exam_exists(
        db,
        test.exam_id,
    ):
        return None

    db_test = Test(
        **test.model_dump()
    )

    db.add(db_test)
    db.commit()
    db.refresh(db_test)

    return db_test


def update_test(
    db: Session,
    test_id: int,
    test: TestUpdate,
):
    db_test = get_test(
        db,
        test_id,
    )

    if db_test is None:
        return None

    update_data = test.model_dump(
        exclude_unset=True
    )

    if (
        "exam_id" in update_data
        and not exam_exists(
            db,
            update_data["exam_id"],
        )
    ):
        return None

    for key, value in update_data.items():
        setattr(
            db_test,
            key,
            value,
        )

    db.commit()
    db.refresh(db_test)

    return db_test


def delete_test(
    db: Session,
    test_id: int,
):
    db_test = get_test(
        db,
        test_id,
    )

    if db_test is None:
        return None

    # ------------------------------------------------------
    # Do not delete a test that already has questions
    # assigned to it.
    # ------------------------------------------------------

    existing_test_question = (
        db.query(TestQuestion)
        .filter(
            TestQuestion.test_id == test_id
        )
        .first()
    )

    if existing_test_question is not None:
        return "HAS_QUESTIONS"

    # ------------------------------------------------------
    # Do not delete a test that already has student attempts.
    # ------------------------------------------------------

    existing_attempt = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.test_id == test_id
        )
        .first()
    )

    if existing_attempt is not None:
        return "HAS_ATTEMPTS"

    # ------------------------------------------------------
    # Safe to delete.
    # ------------------------------------------------------

    db.delete(db_test)
    db.commit()

    return True


def get_test_questions(
    db: Session,
    test_id: int,
):
    test = (
        db.query(Test)
        .filter(Test.id == test_id)
        .first()
    )

    if test is None:
        return None

    return (
        db.query(Question)
        .join(
            TestQuestion,
            TestQuestion.question_id == Question.id,
        )
        .filter(
            TestQuestion.test_id == test_id
        )
        .order_by(
            TestQuestion.display_order
        )
        .all()
    )