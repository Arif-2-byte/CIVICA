from sqlalchemy.orm import Session

from app.models.attempt_question import AttemptQuestion
from app.schemas.attempt_question import AttemptQuestionCreate


def get_attempt_questions(db: Session):
    return db.query(AttemptQuestion).all()


def get_attempt_question(
    db: Session,
    attempt_question_id: int,
):
    return (
        db.query(AttemptQuestion)
        .filter(
            AttemptQuestion.id == attempt_question_id
        )
        .first()
    )


def create_attempt_question(
    db: Session,
    attempt_question: AttemptQuestionCreate,
):
    db_attempt_question = AttemptQuestion(
        **attempt_question.model_dump()
    )

    db.add(db_attempt_question)
    db.commit()
    db.refresh(db_attempt_question)

    return db_attempt_question


def delete_attempt_question(
    db: Session,
    attempt_question_id: int,
):
    db_attempt_question = (
        db.query(AttemptQuestion)
        .filter(
            AttemptQuestion.id == attempt_question_id
        )
        .first()
    )

    if not db_attempt_question:
        return False

    db.delete(db_attempt_question)
    db.commit()

    return True