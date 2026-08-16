from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.models.attempt_question import AttemptQuestion
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.test_attempt import TestAttempt
from app.schemas.attempt_answer import (
    AttemptAnswerCreate,
    AttemptAnswerUpdate,
)


def get_attempt_answers(
    db: Session,
):
    return (
        db.query(AttemptAnswer)
        .order_by(AttemptAnswer.id)
        .all()
    )


def get_attempt_answer(
    db: Session,
    answer_id: int,
):
    answer = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.id == answer_id
        )
        .first()
    )

    if answer is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt Answer not found",
        )

    return answer


def create_attempt_answer(
    db: Session,
    answer: AttemptAnswerCreate,
):
    # Check attempt
    attempt = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.id == answer.attempt_id
        )
        .first()
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Test Attempt not found",
        )

    # Do not allow answers after submission
    if attempt.status == "Submitted":
        raise HTTPException(
            status_code=400,
            detail="Test attempt already submitted",
        )

    # Check that question belongs to this attempt
    attempt_question = (
        db.query(AttemptQuestion)
        .filter(
            AttemptQuestion.attempt_id
            == answer.attempt_id,
            AttemptQuestion.question_id
            == answer.question_id,
        )
        .first()
    )

    if attempt_question is None:
        raise HTTPException(
            status_code=400,
            detail="Question does not belong to this test attempt",
        )

    # Check question
    question = (
        db.query(Question)
        .filter(
            Question.id == answer.question_id
        )
        .first()
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    # If an option was selected, verify it
    if answer.selected_option is not None:
        selected_option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.id
                == answer.selected_option,
                QuestionOption.question_id
                == answer.question_id,
            )
            .first()
        )

        if selected_option is None:
            raise HTTPException(
                status_code=400,
                detail="Selected option does not belong to this question",
            )

    # Check if answer already exists
    existing = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.attempt_id
            == answer.attempt_id,
            AttemptAnswer.question_id
            == answer.question_id,
        )
        .first()
    )

    if existing is not None:
        existing.selected_option = (
            answer.selected_option
        )
        existing.is_marked_for_review = (
            answer.is_marked_for_review
        )

        db.commit()
        db.refresh(existing)

        return existing

    # Create new answer
    db_answer = AttemptAnswer(
        **answer.model_dump()
    )

    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    return db_answer


def update_attempt_answer(
    db: Session,
    answer_id: int,
    answer: AttemptAnswerUpdate,
):
    db_answer = get_attempt_answer(
        db,
        answer_id,
    )

    # Do not modify submitted attempt
    if db_answer.attempt.status == "Submitted":
        raise HTTPException(
            status_code=400,
            detail="Test attempt already submitted",
        )

    update_data = answer.model_dump(
        exclude_unset=True
    )

    # Validate selected option if provided
    if (
        "selected_option" in update_data
        and update_data["selected_option"] is not None
    ):
        selected_option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.id
                == update_data["selected_option"],
                QuestionOption.question_id
                == db_answer.question_id,
            )
            .first()
        )

        if selected_option is None:
            raise HTTPException(
                status_code=400,
                detail="Selected option does not belong to this question",
            )

    for key, value in update_data.items():
        setattr(
            db_answer,
            key,
            value,
        )

    db.commit()
    db.refresh(db_answer)

    return db_answer


def delete_attempt_answer(
    db: Session,
    answer_id: int,
):
    db_answer = get_attempt_answer(
        db,
        answer_id,
    )

    if db_answer.attempt.status == "Submitted":
        raise HTTPException(
            status_code=400,
            detail="Cannot delete answer from submitted attempt",
        )

    db.delete(db_answer)
    db.commit()

    return {
        "message": "Attempt Answer deleted successfully"
    }