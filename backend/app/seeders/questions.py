from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.topic import Topic


QUESTIONS = [
    {
        "topic": "Ancient History",
        "question_text": "The Great Bath is associated with which Harappan site?",
        "option_a": "Harappa",
        "option_b": "Mohenjo-daro",
        "option_c": "Lothal",
        "option_d": "Kalibangan",
        "correct_option": "B",
        "explanation": "The Great Bath is one of the most famous structures found at Mohenjo-daro.",
        "difficulty": "Easy",
        "marks": 2,
        "negative_marks": 0,
        "year": None,
        "source": "CIVICA",
        "is_active": True,
    },
    {
        "topic": "Medieval History",
        "question_text": "Who founded the Mughal Empire in India?",
        "option_a": "Akbar",
        "option_b": "Babur",
        "option_c": "Humayun",
        "option_d": "Sher Shah Suri",
        "correct_option": "B",
        "explanation": "Babur defeated Ibrahim Lodi in the First Battle of Panipat in 1526.",
        "difficulty": "Easy",
        "marks": 2,
        "negative_marks": 0,
        "year": None,
        "source": "CIVICA",
        "is_active": True,
    },
    {
        "topic": "Modern History",
        "question_text": "Who gave the slogan 'Do or Die' during the Quit India Movement?",
        "option_a": "Jawaharlal Nehru",
        "option_b": "Subhas Chandra Bose",
        "option_c": "Mahatma Gandhi",
        "option_d": "Sardar Patel",
        "correct_option": "C",
        "explanation": "Mahatma Gandhi gave the famous 'Do or Die' call in August 1942.",
        "difficulty": "Medium",
        "marks": 2,
        "negative_marks": 0,
        "year": None,
        "source": "CIVICA",
        "is_active": True,
    },
]


def seed_questions(db: Session):
    for question_data in QUESTIONS:

        topic_name = question_data.pop("topic")

        topic = (
            db.query(Topic)
            .filter(Topic.name == topic_name)
            .first()
        )

        if not topic:
            print(f"Topic '{topic_name}' not found. Skipping...")
            continue

        existing = (
            db.query(Question)
            .filter(
                Question.question_text == question_data["question_text"]
            )
            .first()
        )

        if existing:
            continue

        question = Question(
            **question_data,
            topic_id=topic.id,
        )

        db.add(question)

    db.commit()