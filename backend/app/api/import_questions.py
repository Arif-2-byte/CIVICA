from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.import_schema import ImportResponse
from app.services.import_service import QuestionImportService

router = APIRouter(
    prefix="/import",
    tags=["Question Import"],
)


@router.post(
    "/questions",
    response_model=ImportResponse,
)
async def import_questions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    content = await file.read()

    file_content = content.decode("utf-8")

    return QuestionImportService.import_csv(
        db=db,
        file_content=file_content,
    )