from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Category, CurrentAffair
from ..schemas import CurrentAffairCreate, CurrentAffairOut, PaginatedCurrentAffairs

router = APIRouter(prefix="/api/current-affairs", tags=["current-affairs"])


@router.get("", response_model=PaginatedCurrentAffairs)
def list_current_affairs(
    category: Optional[Category] = None,
    exam_tag: Optional[str] = Query(None, description="e.g. UPSC, SSC, Banking"),
    q: Optional[str] = Query(None, description="Search headline and summary"),
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(CurrentAffair)

    if category:
        query = query.filter(CurrentAffair.category == category)
    if exam_tag:
        query = query.filter(CurrentAffair.exam_tags.any(exam_tag))
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(CurrentAffair.headline.ilike(like), CurrentAffair.summary.ilike(like))
        )
    if date_from:
        query = query.filter(CurrentAffair.published_date >= date_from)
    if date_to:
        query = query.filter(CurrentAffair.published_date <= date_to)

    total = query.count()
    items = (
        query.order_by(CurrentAffair.published_date.desc(), CurrentAffair.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedCurrentAffairs(total=total, page=page, page_size=page_size, items=items)


@router.get("/categories", response_model=List[str])
def list_categories():
    return [c.value for c in Category]


@router.get("/{item_id}", response_model=CurrentAffairOut)
def get_current_affair(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CurrentAffair).filter(CurrentAffair.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Current affair item not found")
    return item


@router.post("", response_model=CurrentAffairOut, status_code=201)
def create_current_affair(payload: CurrentAffairCreate, db: Session = Depends(get_db)):
    """Manual/admin creation for now — this is the hook where an AI ingestion
    pipeline (Phase 1.2) will eventually insert auto-summarized articles."""
    item = CurrentAffair(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
