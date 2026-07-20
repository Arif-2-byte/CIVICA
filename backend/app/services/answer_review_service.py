from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.schemas.answer_review import AnswerReview


def get_answer_review(
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

    review = []

    for answer in answers:
        question = answer.question

        if answer.selected_option is None:
            is_correct = False
            marks_awarded = 0

        elif answer.selected_option == question.correct_option:
            is_correct = True
            marks_awarded = question.marks

        else:
            is_correct = False
            marks_awarded = -question.negative_marks

        review.append(
            AnswerReview(
                question_id=question.id,
                question=question.question_text,

                option_a=question.option_a,
                option_b=question.option_b,
                option_c=question.option_c,
                option_d=question.option_d,

                your_answer=answer.selected_option,
                correct_answer=question.correct_option,

                is_correct=is_correct,
                marks_awarded=marks_awarded,

                explanation=question.explanation,
            )
        )

    return review