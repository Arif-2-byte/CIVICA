from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.mistake_notebook import MistakeNotebookResponse
from app.services import mistake_notebook_service


router = APIRouter(
    prefix="/mistakes",
    tags=["Mistake Notebook"],
)


@router.get(
    "/my",
    response_model=list[MistakeNotebookResponse],
)
def get_my_mistakes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return mistake_notebook_service.get_user_mistakes(
        db,
        current_user.id,
    )


@router.get(
    "/{user_id}",
    response_model=list[MistakeNotebookResponse],
)
def get_user_mistakes(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Students can only access their own mistakes.
    # Admins can access any user's mistakes.
    if (
        current_user.id != user_id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to these mistakes.",
        )

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
    current_user: User = Depends(get_current_user),
):
    mistake = mistake_notebook_service.get_mistake(
        db,
        mistake_id,
    )

    if mistake is None:
        raise HTTPException(
            status_code=404,
            detail="Mistake not found",
        )

    if (
        mistake.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this mistake.",
        )

    return mistake_notebook_service.mark_mastered(
        db,
        mistake_id,
    )


@router.patch(
    "/{mistake_id}/revise",
    response_model=MistakeNotebookResponse,
)
def revise_mistake(
    mistake_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mistake = mistake_notebook_service.get_mistake(
        db,
        mistake_id,
    )

    if mistake is None:
        raise HTTPException(
            status_code=404,
            detail="Mistake not found",
        )

    if (
        mistake.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this mistake.",
        )

    return mistake_notebook_service.increase_revision_count(
        db,
        mistake_id,
    )


@router.delete("/{mistake_id}")
def delete_mistake(
    mistake_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mistake = mistake_notebook_service.get_mistake(
        db,
        mistake_id,
    )

    if mistake is None:
        raise HTTPException(
            status_code=404,
            detail="Mistake not found",
        )

    if (
        mistake.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this mistake.",
        )

    return mistake_notebook_service.delete_mistake(
        db,
        mistake_id,
    )