from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.schemas.topic_analytics import TopicAnalytics


def get_topic_analytics(
    db: Session,
    attempt_id: int,
):
    answers = (
        db.query(AttemptAnswer)
        .filter(AttemptAnswer.attempt_id == attempt_id)
        .all()
    )

    if not answers:
        return None

    analytics = {}

    for answer in answers:
        question = answer.question
        topic = question.topic
        subject = topic.subject

        topic_name = topic.name

        if topic_name not in analytics:
            analytics[topic_name] = {
                "topic": topic_name,
                "subject": subject.name,
                "total_questions": 0,
                "correct": 0,
                "wrong": 0,
                "skipped": 0,
                "marks": 0,
            }

        analytics[topic_name]["total_questions"] += 1

        if answer.selected_option is None:
            analytics[topic_name]["skipped"] += 1

        elif answer.selected_option == question.correct_option:
            analytics[topic_name]["correct"] += 1
            analytics[topic_name]["marks"] += question.marks

        else:
            analytics[topic_name]["wrong"] += 1
            analytics[topic_name]["marks"] -= question.negative_marks

    result = []

    for data in analytics.values():
        attempted = data["correct"] + data["wrong"]

        accuracy = (
            round((data["correct"] / attempted) * 100, 2)
            if attempted > 0
            else 0.0
        )

        result.append(
            TopicAnalytics(
                topic=data["topic"],
                subject=data["subject"],
                total_questions=data["total_questions"],
                correct=data["correct"],
                wrong=data["wrong"],
                skipped=data["skipped"],
                marks=data["marks"],
                accuracy=accuracy,
            )
        )

    return result