from app.models.subject import Subject
from app.models.topic import Topic


def seed_topics(db):
    """Seed default topics."""

    if db.query(Topic).count() > 0:
        print("✔ Topics already seeded")
        return

    history = db.query(Subject).filter(Subject.name == "History").first()
    geography = db.query(Subject).filter(Subject.name == "Geography").first()
    polity = db.query(Subject).filter(Subject.name == "Polity").first()
    economy = db.query(Subject).filter(Subject.name == "Economy").first()
    environment = db.query(Subject).filter(Subject.name == "Environment").first()

    topics = []

    if history:
        topics.extend([
            Topic(
                name="Ancient History",
                description="Ancient Indian History",
                difficulty="Easy",
                estimated_time=120,
                subject_id=history.id,
            ),
            Topic(
                name="Medieval History",
                description="Medieval Indian History",
                difficulty="Medium",
                estimated_time=120,
                subject_id=history.id,
            ),
            Topic(
                name="Modern History",
                description="Modern Indian History",
                difficulty="Medium",
                estimated_time=180,
                subject_id=history.id,
            ),
        ])

    if geography:
        topics.extend([
            Topic(
                name="Physical Geography",
                description="Earth and Physical Features",
                difficulty="Medium",
                estimated_time=120,
                subject_id=geography.id,
            ),
            Topic(
                name="Indian Geography",
                description="Geography of India",
                difficulty="Medium",
                estimated_time=120,
                subject_id=geography.id,
            ),
        ])

    if polity:
        topics.extend([
            Topic(
                name="Constitution",
                description="Indian Constitution",
                difficulty="Easy",
                estimated_time=180,
                subject_id=polity.id,
            ),
            Topic(
                name="Fundamental Rights",
                description="Rights and Duties",
                difficulty="Easy",
                estimated_time=90,
                subject_id=polity.id,
            ),
        ])

    if economy:
        topics.extend([
            Topic(
                name="Indian Economy",
                description="Basics of Economy",
                difficulty="Medium",
                estimated_time=150,
                subject_id=economy.id,
            ),
        ])

    if environment:
        topics.extend([
            Topic(
                name="Ecology",
                description="Ecology and Environment",
                difficulty="Easy",
                estimated_time=120,
                subject_id=environment.id,
            ),
            Topic(
                name="Biodiversity",
                description="Biodiversity Conservation",
                difficulty="Medium",
                estimated_time=120,
                subject_id=environment.id,
            ),
        ])

    db.add_all(topics)
    db.commit()

    print("✔ Topics seeded")