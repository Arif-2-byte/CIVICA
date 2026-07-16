from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.models.subject import Subject


SUBJECTS = [
    {
        "name": "History",
        "description": "History for UPSC CSE",
    },
    {
        "name": "Polity",
        "description": "Indian Polity",
    },
    {
        "name": "Geography",
        "description": "Physical and Indian Geography",
    },
    {
        "name": "Economy",
        "description": "Indian Economy",
    },
    {
        "name": "Environment",
        "description": "Environment and Ecology",
    },
    {
        "name": "Science & Technology",
        "description": "Science and Technology",
    },
    {
        "name": "Current Affairs",
        "description": "Current Affairs",
    },
]


def seed_subjects(db: Session):
    upsc_exam = (
        db.query(Exam)
        .filter(Exam.short_name == "UPSC CSE")
        .first()
    )

    if not upsc_exam:
        raise Exception(
            "UPSC CSE exam not found. Run exam seeder first."
        )

    for subject_data in SUBJECTS:

        existing_subject = (
            db.query(Subject)
            .filter(
                Subject.name == subject_data["name"],
                Subject.exam_id == upsc_exam.id,
            )
            .first()
        )

        if existing_subject:
            continue

        subject = Subject(
            name=subject_data["name"],
            description=subject_data["description"],
            exam_id=upsc_exam.id,
        )

        db.add(subject)

    db.commit()