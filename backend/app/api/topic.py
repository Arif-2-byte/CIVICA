from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
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


@router.post("/", response_model=TopicResponse)
def create(
    topic: TopicCreate,
    db: Session = Depends(get_db),
):
    return create_topic(db, topic)


@router.get("/", response_model=list[TopicResponse])
def read_all(
    db: Session = Depends(get_db),
):
    return get_topics(db)


@router.get("/{topic_id}", response_model=TopicResponse)
def read_one(
    topic_id: int,
    db: Session = Depends(get_db),
):
    topic = get_topic(db, topic_id)

    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return topic


@router.put("/{topic_id}", response_model=TopicResponse)
def update(
    topic_id: int,
    topic: TopicCreate,
    db: Session = Depends(get_db),
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


@router.delete("/{topic_id}")
def delete(
    topic_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_topic(
        db,
        topic_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return {
        "message": "Topic deleted successfully"
    }