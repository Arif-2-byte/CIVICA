from app.models.exam import Exam


def seed_exams(db):
    """Seed default exams."""

    if db.query(Exam).count() > 0:
        print("✔ Exams already seeded")
        return

    exams = [
        Exam(
            name="UPSC Civil Services Examination",
            short_name="UPSC CSE",
            description="Union Public Service Commission Civil Services Examination",
            icon="upsc.png",
            is_active=True,
        ),
        Exam(
            name="JKPSC Combined Competitive Examination",
            short_name="JKPSC CCE",
            description="Jammu and Kashmir Public Service Commission",
            icon="jkpsc.png",
            is_active=True,
        ),
        Exam(
            name="SSC Combined Graduate Level",
            short_name="SSC CGL",
            description="Staff Selection Commission Combined Graduate Level",
            icon="ssc.png",
            is_active=True,
        ),
        Exam(
            name="IBPS PO",
            short_name="IBPS",
            description="Institute of Banking Personnel Selection",
            icon="ibps.png",
            is_active=True,
        ),
        Exam(
            name="NEET UG",
            short_name="NEET",
            description="National Eligibility cum Entrance Test",
            icon="neet.png",
            is_active=True,
        ),
    ]

    db.add_all(exams)
    db.commit()

    print("✔ Exams seeded")