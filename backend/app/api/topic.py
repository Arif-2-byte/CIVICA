from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicResponse
from app.services.topic_service import (
    create_topic,
    delete_topic,
    get_topic,
    get_topics,
    update_topic,
)


router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
)


# ==========================================================
# CREATE TOPIC
# Admin only
# ==========================================================

@router.post(
    "/",
    response_model=TopicResponse,
)
def create(
    topic: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return create_topic(
        db,
        topic,
    )


# ==========================================================
# GET ALL TOPICS
# Authenticated users
# ==========================================================

@router.get(
    "/",
    response_model=list[TopicResponse],
)
def read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_topics(db)


# ==========================================================
# GET ONE TOPIC
# Authenticated users
# ==========================================================

@router.get(
    "/{topic_id}",
    response_model=TopicResponse,
)
def read_one(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = get_topic(
        db,
        topic_id,
    )

    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return topic


# ==========================================================
# UPDATE TOPIC
# Admin only
# ==========================================================

@router.put(
    "/{topic_id}",
    response_model=TopicResponse,
)
def update(
    topic_id: int,
    topic: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    updated = update_topic(
        db,
        topic_id,
        topic,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return updated


# ==========================================================
# DELETE TOPIC
# Admin only
# ==========================================================

@router.delete("/{topic_id}")
def delete(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    deleted = delete_topic(
        db,
        topic_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    if deleted == "HAS_QUESTIONS":
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot delete this topic because "
                "it contains questions."
            ),
        )

    return {
        "message": "Topic deleted successfully"
    }