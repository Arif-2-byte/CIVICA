from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.current_affair import CurrentAffair
from app.models.user import User
from app.schemas.current_affair import (
    CurrentAffairCreate,
    CurrentAffairPage,
    CurrentAffairResponse,
)


router = APIRouter(
    prefix="/api/current-affairs",
    tags=["Current affairs"],
)


# ==========================================================
# LIST CURRENT AFFAIRS
# Authenticated users
# ==========================================================

@router.get(
    "",
    response_model=CurrentAffairPage,
)
def list_current_affairs(
    category: str | None = None,
    exam_tag: str | None = Query(
        default=None,
        description="For example: UPSC, SSC, Banking",
    ),
    q: str | None = Query(
        default=None,
        description="Search headline and summary",
    ),
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(CurrentAffair)

    if category:
        query = query.filter(
            CurrentAffair.category == category
        )

    if exam_tag:
        query = query.filter(
            CurrentAffair.exam_tags.any(exam_tag)
        )

    if q:
        term = f"%{q.strip()}%"

        query = query.filter(
            or_(
                CurrentAffair.headline.ilike(term),
                CurrentAffair.summary.ilike(term),
            )
        )

    if date_from:
        query = query.filter(
            CurrentAffair.published_date >= date_from
        )

    if date_to:
        query = query.filter(
            CurrentAffair.published_date <= date_to
        )

    total = query.count()

    items = (
        query
        .order_by(
            CurrentAffair.published_date.desc(),
            CurrentAffair.id.desc(),
        )
        .offset(
            (page - 1) * page_size
        )
        .limit(page_size)
        .all()
    )

    return CurrentAffairPage(
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


# ==========================================================
# LIST CATEGORIES
# Authenticated users
# ==========================================================

@router.get(
    "/categories",
    response_model=list[str],
)
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(CurrentAffair.category)
        .distinct()
        .order_by(
            CurrentAffair.category.asc()
        )
        .all()
    )

    return [
        category
        for (category,) in rows
    ]


# ==========================================================
# GET ONE CURRENT AFFAIR
# Authenticated users
# ==========================================================

@router.get(
    "/{item_id}",
    response_model=CurrentAffairResponse,
)
def get_current_affair(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.get(
        CurrentAffair,
        item_id,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Current affair not found",
        )

    return item


# ==========================================================
# CREATE CURRENT AFFAIR
# Admin only
# ==========================================================

@router.post(
    "",
    response_model=CurrentAffairResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_current_affair(
    payload: CurrentAffairCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    item = CurrentAffair(
        **payload.model_dump()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item