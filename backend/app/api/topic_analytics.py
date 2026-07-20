from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
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
):
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