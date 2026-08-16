from sqlalchemy.orm import Session

from app.models.mistake_notebook import MistakeNotebook


def add_mistake(
    db: Session,
    user_id: int,
    question_id: int,
    attempt_id: int,
):
    """
    Add a question to the mistake notebook.

    Avoid duplicate entries for the same user/question.
    """

    existing = (
        db.query(MistakeNotebook)
        .filter(
            MistakeNotebook.user_id == user_id,
            MistakeNotebook.question_id == question_id,
        )
        .first()
    )

    if existing:
        return existing

    mistake = MistakeNotebook(
        user_id=user_id,
        question_id=question_id,
        attempt_id=attempt_id,
    )

    db.add(mistake)
    db.commit()
    db.refresh(mistake)

    return mistake


def get_mistake(
    db: Session,
    mistake_id: int,
):
    return (
        db.query(MistakeNotebook)
        .filter(
            MistakeNotebook.id == mistake_id
        )
        .first()
    )


def get_user_mistakes(
    db: Session,
    user_id: int,
):
    return (
        db.query(MistakeNotebook)
        .filter(
            MistakeNotebook.user_id == user_id,
            MistakeNotebook.mastered == False,
        )
        .all()
    )


def mark_mastered(
    db: Session,
    mistake_id: int,
):
    mistake = get_mistake(
        db,
        mistake_id,
    )

    if mistake is None:
        return None

    mistake.mastered = True

    db.commit()
    db.refresh(mistake)

    return mistake


def increase_revision_count(
    db: Session,
    mistake_id: int,
):
    mistake = get_mistake(
        db,
        mistake_id,
    )

    if mistake is None:
        return None

    mistake.revision_count += 1

    db.commit()
    db.refresh(mistake)

    return mistake


def delete_mistake(
    db: Session,
    mistake_id: int,
):
    mistake = get_mistake(
        db,
        mistake_id,
    )

    if mistake is None:
        return False

    db.delete(mistake)
    db.commit()

    return True