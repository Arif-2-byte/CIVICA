from sqlalchemy.orm import Session

from app.models.exam import Exam


EXAMS = [
    {
        "name": "UPSC Civil Services Examination",
        "short_name": "UPSC CSE",
        "description": "Union Public Service Commission Civil Services Examination",
        "icon": None,
        "is_active": True,
    },
    {
        "name": "JKPSC Combined Competitive Examination",
        "short_name": "JKPSC CCE",
        "description": "Jammu and Kashmir Public Service Commission",
        "icon": None,
        "is_active": True,
    },
]


def seed_exams(db: Session):
    for exam_data in EXAMS:

        existing_exam = (
            db.query(Exam)
            .filter(Exam.short_name == exam_data["short_name"])
            .first()
        )

        if existing_exam:
            continue

        exam = Exam(**exam_data)
        db.add(exam)

    db.commit()