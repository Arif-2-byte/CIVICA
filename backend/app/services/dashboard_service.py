from sqlalchemy.orm import Session

from app.models.test_attempt import TestAttempt
from app.schemas.dashboard import Dashboard, RecentTest
from app.core.constants import TEST_STATUS_SUBMITTED


def get_dashboard(
    db: Session,
    user_id: int,
):
    attempts = (
        db.query(TestAttempt)
        .filter(TestAttempt.user_id == user_id)
        .all()
    )

    if not attempts:
        return None

    tests_attempted = len(attempts)

    completed_attempts = [
        attempt
        for attempt in attempts
        if attempt.status == TEST_STATUS_SUBMITTED
    ]

    tests_completed = len(completed_attempts)

    highest_score = (
        max((attempt.score for attempt in completed_attempts), default=0)
    )

    average_score = (
        round(
            sum(attempt.score for attempt in completed_attempts)
            / tests_completed,
            2,
        )
        if tests_completed > 0
        else 0.0
    )

    total_correct = sum(
        attempt.total_correct
        for attempt in completed_attempts
    )

    total_wrong = sum(
        attempt.total_wrong
        for attempt in completed_attempts
    )

    total_skipped = sum(
        attempt.total_skipped
        for attempt in completed_attempts
    )

    attempted_questions = total_correct + total_wrong

    average_accuracy = (
        round(
            (total_correct / attempted_questions) * 100,
            2,
        )
        if attempted_questions > 0
        else 0.0
    )

    recent_attempts = sorted(
        completed_attempts,
        key=lambda x: x.submitted_at or x.started_at,
        reverse=True,
    )[:5]

    recent_tests = [
        RecentTest(
            attempt_id=attempt.id,
            test_name=attempt.test.title,
            score=attempt.score,
            status=attempt.status,
            submitted_at=attempt.submitted_at,
        )
        for attempt in recent_attempts
    ]

    return Dashboard(
        tests_attempted=tests_attempted,
        tests_completed=tests_completed,
        average_score=average_score,
        highest_score=highest_score,
        average_accuracy=average_accuracy,
        total_correct=total_correct,
        total_wrong=total_wrong,
        total_skipped=total_skipped,
        recent_tests=recent_tests,
    )