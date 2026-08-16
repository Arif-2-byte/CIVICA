from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.models.question import Question
from app.schemas.topic import TopicCreate


def create_topic(
    db: Session,
    topic: TopicCreate,
):
    db_topic = Topic(
        name=topic.name,
        description=topic.description,
        difficulty=topic.difficulty,
        estimated_time=topic.estimated_time,
        subject_id=topic.subject_id,
    )

    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)

    return db_topic


def get_topics(
    db: Session,
):
    return db.query(Topic).all()


def get_topic(
    db: Session,
    topic_id: int,
):
    return (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )


def update_topic(
    db: Session,
    topic_id: int,
    topic: TopicCreate,
):
    db_topic = get_topic(
        db,
        topic_id,
    )

    if not db_topic:
        return None

    db_topic.name = topic.name
    db_topic.description = topic.description
    db_topic.difficulty = topic.difficulty
    db_topic.estimated_time = topic.estimated_time
    db_topic.subject_id = topic.subject_id

    db.commit()
    db.refresh(db_topic)

    return db_topic


def delete_topic(
    db: Session,
    topic_id: int,
):
    db_topic = get_topic(
        db,
        topic_id,
    )

    if not db_topic:
        return None

    # ------------------------------------------------------
    # Do not delete a topic that already contains questions.
    # ------------------------------------------------------

    existing_question = (
        db.query(Question)
        .filter(
            Question.topic_id == topic_id
        )
        .first()
    )

    if existing_question is not None:
        return "HAS_QUESTIONS"

    # ------------------------------------------------------
    # Safe to delete.
    # ------------------------------------------------------

    db.delete(db_topic)
    db.commit()

    return True