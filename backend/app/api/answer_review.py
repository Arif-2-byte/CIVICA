from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.answer_review import AnswerReview
from app.services import answer_review_service

router = APIRouter(
    prefix="/answer-review",
    tags=["Answer Review"],
)


@router.get(
    "/{attempt_id}",
    response_model=list[AnswerReview],
)
def review_answers(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    review = answer_review_service.get_answer_review(
        db=db,
        attempt_id=attempt_id,
    )

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="No answers found for this attempt.",
        )

    return review