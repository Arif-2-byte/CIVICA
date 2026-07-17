from sqlalchemy.orm import Session

from app.models.test_attempt import TestAttempt
from app.models.test import Test
from app.schemas.result import ResultSummary


def get_result_summary(db: Session, attempt_id: int):
    attempt = (
        db.query(TestAttempt)
        .filter(TestAttempt.id == attempt_id)
        .first()
    )

    if not attempt:
        return None

    test = (
        db.query(Test)
        .filter(Test.id == attempt.test_id)
        .first()
    )

    if not test:
        return None

    total_marks = test.total_marks if test.total_marks else 0

    percentage = (
        (attempt.score / total_marks) * 100
        if total_marks > 0
        else 0
    )

    attempted_questions = (
        attempt.total_correct + attempt.total_wrong
    )

    accuracy = (
        (attempt.total_correct / attempted_questions) * 100
        if attempted_questions > 0
        else 0
    )

    return ResultSummary(
        attempt_id=attempt.id,
        user_id=attempt.user_id,
        test_id=attempt.test_id,
        score=attempt.score,
        total_marks=total_marks,
        percentage=round(percentage, 2),
        correct=attempt.total_correct,
        wrong=attempt.total_wrong,
        skipped=attempt.total_skipped,
        accuracy=round(accuracy, 2),
        status=attempt.status,
    )