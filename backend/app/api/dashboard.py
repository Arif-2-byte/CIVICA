from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.dashboard import Dashboard
from app.services import dashboard_service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/{user_id}",
    response_model=Dashboard,
)
def get_dashboard(
    user_id: int,
    db: Session = Depends(get_db),
):
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