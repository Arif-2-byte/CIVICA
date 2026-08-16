from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import Dashboard
from app.services import dashboard_service


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/my",
    response_model=Dashboard,
)
def get_my_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dashboard = dashboard_service.get_dashboard(
        db=db,
        user_id=current_user.id,
    )

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="No test attempts found for this user.",
        )

    return dashboard


@router.get(
    "/{user_id}",
    response_model=Dashboard,
)
def get_dashboard(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (
        current_user.id != user_id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this dashboard",
        )

    dashboard = dashboard_service.get_dashboard(
        db=db,
        user_id=user_id,
    )

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="No test attempts found for this user.",
        )

    return dashboard