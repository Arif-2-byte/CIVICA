from sqlalchemy.orm import Session

from app.models.exam import Exam


def seed_exams(db: Session):
    exams = [
        ("Union Public Service Commission", "UPSC"),
        ("Jammu and Kashmir Public Service Commission", "JKPSC"),
        ("Staff Selection Commission Common Level Examination", "SSC"),
        ("Banking Probationary Officers", "BANK"),
        ("National Eligibility cum Entrance Test", "NEET"),
        ("Joint Entrance Examination", "JEE"),
        ("Common University Entrance Test", "CUET"),
    ]

    for name, short_name in exams:
        exists = db.query(Exam).filter(
            Exam.short_name == short_name
        ).first()

        if not exists:
            db.add(
                Exam(
                    name=name,
                    short_name=short_name,
                    description=f"{name} Examination",
                )
            )

    db.commit()