from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.models.topic import Topic
from app.schemas.subject import SubjectCreate


def create_subject(
    db: Session,
    subject: SubjectCreate,
):
    db_subject = Subject(
        name=subject.name,
        description=subject.description,
        exam_id=subject.exam_id,
    )

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    return db_subject


def get_subjects(
    db: Session,
):
    return db.query(Subject).all()


def get_subject(
    db: Session,
    subject_id: int,
):
    return (
        db.query(Subject)
        .filter(
            Subject.id == subject_id
        )
        .first()
    )


def update_subject(
    db: Session,
    subject_id: int,
    subject: SubjectCreate,
):
    db_subject = get_subject(
        db,
        subject_id,
    )

    if not db_subject:
        return None

    db_subject.name = subject.name
    db_subject.description = subject.description
    db_subject.exam_id = subject.exam_id

    db.commit()
    db.refresh(db_subject)

    return db_subject


def delete_subject(
    db: Session,
    subject_id: int,
):
    db_subject = get_subject(
        db,
        subject_id,
    )

    if not db_subject:
        return None

    # ------------------------------------------------------
    # Do not delete a subject that already contains topics.
    # ------------------------------------------------------

    existing_topic = (
        db.query(Topic)
        .filter(
            Topic.subject_id == subject_id
        )
        .first()
    )

    if existing_topic is not None:
        return "HAS_TOPICS"

    # ------------------------------------------------------
    # Safe to delete.
    # ------------------------------------------------------

    db.delete(db_subject)
    db.commit()

    return True