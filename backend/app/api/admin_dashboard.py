from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.jwt_handler import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.admin_dashboard import AdminDashboard
from app.services import admin_dashboard_service


router = APIRouter(
    prefix="/admin-dashboard",
    tags=["Admin Dashboard"],
)


@router.get(
    "/",
    response_model=AdminDashboard,
)
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return admin_dashboard_service.get_admin_dashboard(
        db
    )