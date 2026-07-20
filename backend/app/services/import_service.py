from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.question import Question

from app.schemas.import_schema import (
    ImportErrorItem,
    ImportSummary,
    ImportResponse,
)

from app.utils.csv_validator import validate_csv


class QuestionImportService:

    @staticmethod
    def import_csv(
        db: Session,
        file_content: str,
    ) -> ImportResponse:

        validation = validate_csv(file_content)

        rows = validation["rows"]
        validation_errors = validation["errors"]

        imported = 0
        duplicates = 0

        errors = []

        # Validation errors
        for error in validation_errors:
            errors.append(
                ImportErrorItem(
                    row=0,
                    message=error,
                )
            )

        if validation_errors:
            return ImportResponse(
                success=False,
                summary=ImportSummary(
                    total_rows=0,
                    imported=0,
                    duplicates=0,
                    failed=len(validation_errors),
                ),
                errors=errors,
            )

        for index, row in enumerate(rows, start=2):

            exam = (
                db.query(Exam)
                .filter(
                    Exam.name == row["exam"].strip()
                )
                .first()
            )

            if not exam:
                errors.append(
                    ImportErrorItem(
                        row=index,
                        message=f"Exam '{row['exam']}' not found.",
                    )
                )
                continue

            subject = (
                db.query(Subject)
                .filter(
                    Subject.name == row["subject"].strip(),
                    Subject.exam_id == exam.id,
                )
                .first()
            )

            if not subject:
                errors.append(
                    ImportErrorItem(
                        row=index,
                        message=f"Subject '{row['subject']}' not found.",
                    )
                )
                continue

            topic = (
                db.query(Topic)
                .filter(
                    Topic.name == row["topic"].strip(),
                    Topic.subject_id == subject.id,
                )
                .first()
            )

            if not topic:
                errors.append(
                    ImportErrorItem(
                        row=index,
                        message=f"Topic '{row['topic']}' not found.",
                    )
                )
                continue

            duplicate = (
                db.query(Question)
                .filter(
                    Question.question_text == row["question_text"].strip(),
                    Question.topic_id == topic.id,
                )
                .first()
            )

            if duplicate:
                duplicates += 1
                continue

            question = Question(
                topic_id=topic.id,
                question_text=row["question_text"].strip(),
                option_a=row["option_a"].strip(),
                option_b=row["option_b"].strip(),
                option_c=row["option_c"].strip(),
                option_d=row["option_d"].strip(),
                correct_answer=row["correct_answer"].strip().upper(),
                explanation=row["explanation"].strip(),
            )

            db.add(question)
            imported += 1

        db.commit()

        return ImportResponse(
            success=True,
            summary=ImportSummary(
                total_rows=len(rows),
                imported=imported,
                duplicates=duplicates,
                failed=len(errors),
            ),
            errors=errors,
        )