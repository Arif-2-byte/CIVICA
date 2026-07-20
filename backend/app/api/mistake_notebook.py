from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.mistake_notebook import MistakeNotebookResponse
from app.services import mistake_notebook_service

router = APIRouter(
    prefix="/mistakes",
    tags=["Mistake Notebook"],
)


@router.get(
    "/{user_id}",
    response_model=list[MistakeNotebookResponse],
)
def get_user_mistakes(
    user_id: int,
    db: Session = Depends(get_db),
):
    return mistake_notebook_service.get_user_mistakes(
        db,
        user_id,
    )


@router.patch(
    "/{mistake_id}/master",
    response_model=MistakeNotebookResponse,
)
def mark_mastered(
    mistake_id: int,
    db: Session = Depends(get_db),
):
    mistake = mistake_notebook_service.mark_mastered(
        db,
        mistake_id,
    )

    if not mistake:
        raise HTTPException(
            status_code=404,
            detail="Mistake not found",
        )

    return mistake


@router.patch(
    "/{mistake_id}/revise",
    response_model=MistakeNotebookResponse,
)
def revise_mistake(
    mistake_id: int,
    db: Session = Depends(get_db),
):
    mistake = mistake_notebook_service.increase_revision_count(
        db,
        mistake_id,
    )

    if not mistake:
        raise HTTPException(
            status_code=404,
            detail="Mistake not found",
        )

    return mistake


@router.delete("/{mistake_id}")
def delete_mistake(
    mistake_id: int,
    db: Session = Depends(get_db),
):
    deleted = mistake_notebook_service.delete_mistake(
        db,
        mistake_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Mistake not found",
        )

    return {
        "message": "Mistake deleted successfully"
    }