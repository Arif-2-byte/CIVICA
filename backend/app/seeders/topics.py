from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.models.topic import Topic


TOPICS = {
    "History": [
        "Ancient History",
        "Medieval History",
        "Modern History",
        "Art & Culture",
    ],
    "Polity": [
        "Constitution",
        "Fundamental Rights",
        "Parliament",
        "Judiciary",
    ],
    "Geography": [
        "Physical Geography",
        "Indian Geography",
        "World Geography",
    ],
    "Economy": [
        "Macroeconomics",
        "Banking",
        "Budget",
        "Taxation",
    ],
    "Environment": [
        "Ecology",
        "Biodiversity",
        "Climate Change",
    ],
    "Science & Technology": [
        "Space Technology",
        "Biotechnology",
        "Artificial Intelligence",
    ],
    "Current Affairs": [
        "National",
        "International",
        "Government Schemes",
    ],
}


def seed_topics(db: Session):
    for subject_name, topic_names in TOPICS.items():

        subject = (
            db.query(Subject)
            .filter(Subject.name == subject_name)
            .first()
        )

        if not subject:
            print(f"Subject '{subject_name}' not found. Skipping...")
            continue

        for topic_name in topic_names:

            existing_topic = (
                db.query(Topic)
                .filter(
                    Topic.name == topic_name,
                    Topic.subject_id == subject.id,
                )
                .first()
            )

            if existing_topic:
                continue

            topic = Topic(
                name=topic_name,
                description=f"{topic_name} topics",
                difficulty="Medium",
                estimated_time=60,
                is_active=True,
                subject_id=subject.id,
            )

            db.add(topic)

    db.commit()