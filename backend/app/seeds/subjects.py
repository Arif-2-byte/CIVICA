from app.models.exam import Exam
from app.models.subject import Subject


def seed_subjects(db):
    """Seed default subjects for each exam."""

    if db.query(Subject).count() > 0:
        print("✔ Subjects already seeded")
        return

    upsc = db.query(Exam).filter(Exam.short_name == "UPSC CSE").first()
    jkpsc = db.query(Exam).filter(Exam.short_name == "JKPSC CCE").first()
    ssc = db.query(Exam).filter(Exam.short_name == "SSC CGL").first()

    if not upsc or not jkpsc or not ssc:
        print("❌ Seed exams first.")
        return

    subjects = [
        # UPSC
        Subject(
            name="History",
            description="Ancient, Medieval and Modern Indian History",
            exam_id=upsc.id,
        ),
        Subject(
            name="Geography",
            description="Physical and Indian Geography",
            exam_id=upsc.id,
        ),
        Subject(
            name="Polity",
            description="Indian Constitution and Governance",
            exam_id=upsc.id,
        ),
        Subject(
            name="Economy",
            description="Indian Economy",
            exam_id=upsc.id,
        ),
        Subject(
            name="Environment",
            description="Ecology and Environment",
            exam_id=upsc.id,
        ),

        # JKPSC
        Subject(
            name="History",
            description="History for JKPSC",
            exam_id=jkpsc.id,
        ),
        Subject(
            name="Polity",
            description="Indian Polity",
            exam_id=jkpsc.id,
        ),
        Subject(
            name="Geography",
            description="Geography",
            exam_id=jkpsc.id,
        ),

        # SSC
        Subject(
            name="General Awareness",
            description="SSC General Awareness",
            exam_id=ssc.id,
        ),
        Subject(
            name="General Science",
            description="SSC General Science",
            exam_id=ssc.id,
        ),
    ]

    db.add_all(subjects)
    db.commit()

    print("✔ Subjects seeded")