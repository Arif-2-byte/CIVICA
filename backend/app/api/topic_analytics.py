from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_current_user
from app.db.session import get_db
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.schemas.topic_analytics import TopicAnalytics
from app.services import topic_analytics_service


router = APIRouter(
    prefix="/topic-analytics",
    tags=["Topic Analytics"],
)


@router.get(
    "/{attempt_id}",
    response_model=list[TopicAnalytics],
)
def get_topic_analytics(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ------------------------------------------------------
    # Find the attempt
    # ------------------------------------------------------

    attempt = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.id == attempt_id
        )
        .first()
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt not found.",
        )

    # ------------------------------------------------------
    # Students can only view their own analytics.
    # Admin can view any attempt.
    # ------------------------------------------------------

    if (
        attempt.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this analytics.",
        )

    # ------------------------------------------------------
    # Get analytics
    # ------------------------------------------------------

    analytics = topic_analytics_service.get_topic_analytics(
        db=db,
        attempt_id=attempt_id,
    )

    if analytics is None:
        raise HTTPException(
            status_code=404,
            detail="No answers found for this attempt.",
        )

    return analytics