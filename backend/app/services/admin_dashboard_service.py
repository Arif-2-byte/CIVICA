from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.constants import TEST_STATUS_SUBMITTED
from app.models.user import User
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt


def get_admin_dashboard(
    db: Session,
):
    total_users = (
        db.query(User)
        .count()
    )

    total_exams = (
        db.query(Exam)
        .count()
    )

    total_subjects = (
        db.query(Subject)
        .count()
    )

    total_topics = (
        db.query(Topic)
        .count()
    )

    total_questions = (
        db.query(Question)
        .count()
    )

    total_tests = (
        db.query(Test)
        .count()
    )

    total_attempts = (
        db.query(TestAttempt)
        .count()
    )

    completed_attempts = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.status
            == TEST_STATUS_SUBMITTED
        )
        .count()
    )

    average_score = (
        db.query(
            func.avg(TestAttempt.score)
        )
        .filter(
            TestAttempt.status
            == TEST_STATUS_SUBMITTED
        )
        .scalar()
    )

    return {
        "total_users": total_users,
        "total_exams": total_exams,
        "total_subjects": total_subjects,
        "total_topics": total_topics,
        "total_questions": total_questions,
        "total_tests": total_tests,
        "total_attempts": total_attempts,
        "completed_attempts": completed_attempts,
        "average_score": round(
            float(average_score or 0),
            2,
        ),
    }