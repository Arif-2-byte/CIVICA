from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.test_session import TestSessionResponse
from app.services.test_session_service import get_test_session


router = APIRouter(
    prefix="/test-session",
    tags=["Test Session"],
)


@router.get(
    "/{attempt_id}",
    response_model=TestSessionResponse,
)
def get_session(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_test_session(
        db=db,
        attempt_id=attempt_id,
        user_id=current_user.id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Test session not found",
        )

    return session