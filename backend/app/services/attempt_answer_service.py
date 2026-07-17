from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.schemas.attempt_answer import (
    AttemptAnswerCreate,
    AttemptAnswerUpdate,
)


def get_attempt_answers(db: Session):
    return db.query(AttemptAnswer).all()


def get_attempt_answer(db: Session, answer_id: int):
    answer = (
        db.query(AttemptAnswer)
        .filter(AttemptAnswer.id == answer_id)
        .first()
    )

    if not answer:
        raise HTTPException(
            status_code=404,
            detail="Attempt Answer not found",
        )

    return answer


def create_attempt_answer(
    db: Session,
    answer: AttemptAnswerCreate,
):
    attempt = (
        db.query(TestAttempt)
        .filter(TestAttempt.id == answer.attempt_id)
        .first()
    )

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Test Attempt not found",
        )

    question = (
        db.query(Question)
        .filter(Question.id == answer.question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    existing = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.attempt_id == answer.attempt_id,
            AttemptAnswer.question_id == answer.question_id,
        )
        .first()
    )

    if existing:
        return existing

    db_answer = AttemptAnswer(**answer.model_dump())

    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    return db_answer


def update_attempt_answer(
    db: Session,
    answer_id: int,
    answer: AttemptAnswerUpdate,
):
    db_answer = (
        db.query(AttemptAnswer)
        .filter(AttemptAnswer.id == answer_id)
        .first()
    )

    if not db_answer:
        raise HTTPException(
            status_code=404,
            detail="Attempt Answer not found",
        )

    update_data = answer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_answer, key, value)

    db.commit()
    db.refresh(db_answer)

    return db_answer


def delete_attempt_answer(
    db: Session,
    answer_id: int,
):
    db_answer = (
        db.query(AttemptAnswer)
        .filter(AttemptAnswer.id == answer_id)
        .first()
    )

    if not db_answer:
        raise HTTPException(
            status_code=404,
            detail="Attempt Answer not found",
        )

    db.delete(db_answer)
    db.commit()

    return {
        "message": "Attempt Answer deleted successfully"
    }