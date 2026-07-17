from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.result import ResultSummary
from app.services import result_service

router = APIRouter(
    prefix="/results",
    tags=["Results"],
)


@router.get(
    "/{attempt_id}",
    response_model=ResultSummary,
)
def get_result(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    result = result_service.get_result_summary(
        db,
        attempt_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found",
        )

    return result