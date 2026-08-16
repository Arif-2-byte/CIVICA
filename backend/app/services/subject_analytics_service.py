from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.models.question_option import QuestionOption
from app.schemas.subject_analytics import SubjectAnalytics


def get_subject_analytics(
    db: Session,
    attempt_id: int,
):
    answers = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.attempt_id == attempt_id
        )
        .all()
    )

    if not answers:
        return None

    analytics = {}

    for answer in answers:
        question = answer.question

        if question is None:
            continue

        topic = question.topic

        if topic is None:
            continue

        subject = topic.subject

        if subject is None:
            continue

        subject_name = subject.name

        if subject_name not in analytics:
            analytics[subject_name] = {
                "subject": subject_name,
                "total_questions": 0,
                "correct": 0,
                "wrong": 0,
                "skipped": 0,
                "marks": 0.0,
            }

        data = analytics[subject_name]

        data["total_questions"] += 1

        # Skipped
        if answer.selected_option is None:
            data["skipped"] += 1
            continue

        # Find selected option
        selected_option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.id
                == answer.selected_option,
                QuestionOption.question_id
                == question.id,
            )
            .first()
        )

        # Invalid option is treated as wrong
        if selected_option is None:
            data["wrong"] += 1
            data["marks"] -= float(
                question.negative_marks
            )
            continue

        # Correct
        if selected_option.is_correct:
            data["correct"] += 1
            data["marks"] += float(
                question.marks
            )

        # Wrong
        else:
            data["wrong"] += 1
            data["marks"] -= float(
                question.negative_marks
            )

    result = []

    for data in analytics.values():

        attempted = (
            data["correct"]
            + data["wrong"]
        )

        accuracy = (
            round(
                (
                    data["correct"]
                    / attempted
                )
                * 100,
                2,
            )
            if attempted > 0
            else 0.0
        )

        result.append(
            SubjectAnalytics(
                subject=data["subject"],
                total_questions=data[
                    "total_questions"
                ],
                correct=data["correct"],
                wrong=data["wrong"],
                skipped=data["skipped"],
                marks=round(
                    data["marks"],
                    2,
                ),
                accuracy=accuracy,
            )
        )

    return result