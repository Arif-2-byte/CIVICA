from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.topic import Topic
from app.schemas.question import QuestionCreate, QuestionUpdate


def create_question(db: Session, question: QuestionCreate):
    db_question = Question(**question.model_dump())

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question


def get_question(db: Session, question_id: int):
    return (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Question)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_question(
    db: Session,
    question_id: int,
    question: QuestionUpdate,
):
    db_question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if not db_question:
        return None

    update_data = question.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)

    return db_question


def delete_question(db: Session, question_id: int):
    db_question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if not db_question:
        return None

    db.delete(db_question)
    db.commit()

    return db_question


def topic_exists(db: Session, topic_id: int) -> bool:
    return db.query(Topic.id).filter(Topic.id == topic_id).first() is not None
