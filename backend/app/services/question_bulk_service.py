from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.test_question import TestQuestion
from app.models.attempt_question import AttemptQuestion


def bulk_delete_questions(
    db: Session,
    question_ids: list[int],
) -> int:
    """
    Permanently delete multiple questions.

    Questions already assigned to tests or used in
    student attempts are skipped.
    Returns the number of deleted records.
    """

    if not question_ids:
        return 0

    # ------------------------------------------------------
    # Find questions that are already assigned to tests
    # ------------------------------------------------------

    assigned_question_ids = {
        question_id
        for (question_id,) in (
            db.query(TestQuestion.question_id)
            .filter(
                TestQuestion.question_id.in_(question_ids)
            )
            .all()
        )
    }

    # ------------------------------------------------------
    # Find questions already used in student attempts
    # ------------------------------------------------------

    attempted_question_ids = {
        question_id
        for (question_id,) in (
            db.query(AttemptQuestion.question_id)
            .filter(
                AttemptQuestion.question_id.in_(question_ids)
            )
            .all()
        )
    }

    protected_ids = (
        assigned_question_ids
        | attempted_question_ids
    )

    # ------------------------------------------------------
    # Only delete safe questions
    # ------------------------------------------------------

    safe_question_ids = [
        question_id
        for question_id in question_ids
        if question_id not in protected_ids
    ]

    if not safe_question_ids:
        return 0

    deleted = (
        db.query(Question)
        .filter(
            Question.id.in_(safe_question_ids)
        )
        .delete(
            synchronize_session=False
        )
    )

    db.commit()

    return deleted


def bulk_activate_questions(
    db: Session,
    question_ids: list[int],
) -> int:
    """
    Activate multiple questions.
    """

    if not question_ids:
        return 0

    updated = (
        db.query(Question)
        .filter(
            Question.id.in_(question_ids)
        )
        .update(
            {"is_active": True},
            synchronize_session=False,
        )
    )

    db.commit()

    return updated


def bulk_deactivate_questions(
    db: Session,
    question_ids: list[int],
) -> int:
    """
    Deactivate multiple questions.
    """

    if not question_ids:
        return 0

    updated = (
        db.query(Question)
        .filter(
            Question.id.in_(question_ids)
        )
        .update(
            {"is_active": False},
            synchronize_session=False,
        )
    )

    db.commit()

    return updated