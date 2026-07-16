from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.schemas.test_question import (
    TestQuestionCreate,
    TestQuestionUpdate,
)


def get_test_questions(db: Session):
    return db.query(TestQuestion).all()


def get_test_question(
    db: Session,
    test_question_id: int,
):
    return (
        db.query(TestQuestion)
        .filter(TestQuestion.id == test_question_id)
        .first()
    )


def create_test_question(
    db: Session,
    test_question: TestQuestionCreate,
):
    # Check if Test exists
    test = (
        db.query(Test)
        .filter(Test.id == test_question.test_id)
        .first()
    )

    if not test:
        return None

    # Check if Question exists
    question = (
        db.query(Question)
        .filter(Question.id == test_question.question_id)
        .first()
    )

    if not question:
        return None

    # Prevent duplicate questions in the same test
    existing = (
        db.query(TestQuestion)
        .filter(
            TestQuestion.test_id == test_question.test_id,
            TestQuestion.question_id == test_question.question_id,
        )
        .first()
    )

    if existing:
        return existing

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
    db_test_question = (
        db.query(TestQuestion)
        .filter(TestQuestion.id == test_question_id)
        .first()
    )

    if not db_test_question:
        return None

    update_data = test_question.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_test_question, key, value)

    db.commit()
    db.refresh(db_test_question)

    return db_test_question


def delete_test_question(
    db: Session,
    test_question_id: int,
):
    db_test_question = (
        db.query(TestQuestion)
        .filter(TestQuestion.id == test_question_id)
        .first()
    )

    if not db_test_question:
        return False

    db.delete(db_test_question)
    db.commit()

    return True