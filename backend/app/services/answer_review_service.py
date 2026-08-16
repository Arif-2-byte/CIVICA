from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.models.question_option import QuestionOption
from app.schemas.answer_review import AnswerReview


def get_answer_review(
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

    review = []

    for answer in answers:

        question = answer.question

        if question is None:
            continue

        # --------------------------------------------------
        # Get all options for this question
        # --------------------------------------------------

        options = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.question_id == question.id
            )
            .order_by(
                QuestionOption.display_order
            )
            .all()
        )

        # --------------------------------------------------
        # Find selected option
        # --------------------------------------------------

        selected_option = None

        if answer.selected_option is not None:
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

        # --------------------------------------------------
        # Find correct option
        # --------------------------------------------------

        correct_option = next(
            (
                option
                for option in options
                if option.is_correct
            ),
            None,
        )

        # --------------------------------------------------
        # Evaluate answer
        # --------------------------------------------------

        if selected_option is None:
            is_correct = False
            marks_awarded = 0.0

        elif selected_option.is_correct:
            is_correct = True
            marks_awarded = question.marks

        else:
            is_correct = False
            marks_awarded = -question.negative_marks

        # --------------------------------------------------
        # Build option data
        # --------------------------------------------------

        option_a = (
            options[0].option_text
            if len(options) > 0
            else None
        )

        option_b = (
            options[1].option_text
            if len(options) > 1
            else None
        )

        option_c = (
            options[2].option_text
            if len(options) > 2
            else None
        )

        option_d = (
            options[3].option_text
            if len(options) > 3
            else None
        )

        review.append(
            AnswerReview(
                question_id=question.id,
                question=question.question_text,

                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,

                your_answer=(
                    answer.selected_option
                    if answer.selected_option is not None
                    else None
                ),

                correct_answer=(
                    correct_option.id
                    if correct_option is not None
                    else None
                ),

                is_correct=is_correct,
                marks_awarded=marks_awarded,

                explanation=question.explanation,
            )
        )

    return review