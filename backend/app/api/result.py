from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_current_user
from app.db.session import get_db
from app.models.user import User
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
    current_user: User = Depends(get_current_user),
):
    result = result_service.get_result_summary(
        db=db,
        attempt_id=attempt_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found",
        )

    # Student can only access their own result.
    # Admin can access any result.
    if (
        result["user_id"] != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this result",
        )

    return result