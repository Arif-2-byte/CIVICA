from pydantic import BaseModel
from typing import List


class ImportErrorItem(BaseModel):
    row: int
    message: str


class ImportSummary(BaseModel):
    total_rows: int
    imported: int
    duplicates: int
    failed: int


class ImportResponse(BaseModel):
    success: bool
    summary: ImportSummary
    errors: List[ImportErrorItem] = []