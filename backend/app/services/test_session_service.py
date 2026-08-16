from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.models.attempt_question import AttemptQuestion
from app.models.question_option import QuestionOption
from app.models.test import Test
from app.models.test_attempt import TestAttempt


def get_test_session(
    db: Session,
    attempt_id: int,
    user_id: int,
):
    # Get attempt
    attempt = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.id == attempt_id,
            TestAttempt.user_id == user_id,
        )
        .first()
    )

    if attempt is None:
        return None

    # Get test
    test = (
        db.query(Test)
        .filter(
            Test.id == attempt.test_id
        )
        .first()
    )

    if test is None:
        return None

    # Get questions in display order
    attempt_questions = (
        db.query(AttemptQuestion)
        .filter(
            AttemptQuestion.attempt_id
            == attempt_id
        )
        .order_by(
            AttemptQuestion.display_order
        )
        .all()
    )

    questions = []

    for attempt_question in attempt_questions:

        question = attempt_question.question

        if question is None:
            continue

        options = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.question_id
                == question.id
            )
            .order_by(
                QuestionOption.id
            )
            .all()
        )

        answer = (
            db.query(AttemptAnswer)
            .filter(
                AttemptAnswer.attempt_id
                == attempt_id,
                AttemptAnswer.question_id
                == question.id,
            )
            .first()
        )

        questions.append(
            {
                "attempt_question_id": (
                    attempt_question.id
                ),
                "question_id": question.id,
                "display_order": (
                    attempt_question.display_order
                ),
                "question_text": (
                    question.question_text
                ),
                "marks": question.marks,
                "negative_marks": (
                    question.negative_marks
                ),
                "options": [
                    {
                        "id": option.id,
                        "option_text": (
                            option.option_text
                        ),
                    }
                    for option in options
                ],
                "selected_option": (
                    answer.selected_option
                    if answer
                    else None
                ),
                "is_marked_for_review": (
                    answer.is_marked_for_review
                    if answer
                    else False
                ),
            }
        )

    return {
        "attempt_id": attempt.id,
        "test_id": test.id,
        "title": test.title,
        "description": test.description,
        "duration": test.duration,
        "total_questions": (
            test.total_questions
        ),
        "total_marks": test.total_marks,
        "status": attempt.status,
        "started_at": attempt.started_at,
        "questions": questions,
    }