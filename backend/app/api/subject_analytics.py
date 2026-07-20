from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.subject_analytics import SubjectAnalytics
from app.services import subject_analytics_service

router = APIRouter(
    prefix="/subject-analytics",
    tags=["Subject Analytics"],
)


@router.get(
    "/{attempt_id}",
    response_model=list[SubjectAnalytics],
)
def get_subject_analytics(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    analytics = subject_analytics_service.get_subject_analytics(
        db=db,
        attempt_id=attempt_id,
    )

    if analytics is None:
        raise HTTPException(
            status_code=404,
            detail="No answers found for this attempt.",
        )

    return analytics