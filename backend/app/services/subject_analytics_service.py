from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.schemas.subject_analytics import SubjectAnalytics


def get_subject_analytics(
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

        subject_name = subject.name

        if subject_name not in analytics:
            analytics[subject_name] = {
                "subject": subject_name,
                "total_questions": 0,
                "correct": 0,
                "wrong": 0,
                "skipped": 0,
                "marks": 0,
            }

        analytics[subject_name]["total_questions"] += 1

        if answer.selected_option is None:
            analytics[subject_name]["skipped"] += 1

        elif answer.selected_option == question.correct_option:
            analytics[subject_name]["correct"] += 1
            analytics[subject_name]["marks"] += question.marks

        else:
            analytics[subject_name]["wrong"] += 1
            analytics[subject_name]["marks"] -= question.negative_marks

    result = []

    for data in analytics.values():
        attempted = data["correct"] + data["wrong"]

        accuracy = (
            round((data["correct"] / attempted) * 100, 2)
            if attempted > 0
            else 0.0
        )

        result.append(
            SubjectAnalytics(
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