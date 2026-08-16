from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.subject import Subject
from app.models.topic import Topic

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

        # --------------------------------------------------
        # Validation errors
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Process each row
        # --------------------------------------------------

        for index, row in enumerate(
            rows,
            start=2,
        ):

            try:

                # ------------------------------------------
                # Find Exam
                # ------------------------------------------

                exam = (
                    db.query(Exam)
                    .filter(
                        Exam.name
                        == row["exam"].strip()
                    )
                    .first()
                )

                if exam is None:
                    errors.append(
                        ImportErrorItem(
                            row=index,
                            message=(
                                f"Exam "
                                f"'{row['exam']}' "
                                f"not found."
                            ),
                        )
                    )
                    continue

                # ------------------------------------------
                # Find Subject
                # ------------------------------------------

                subject = (
                    db.query(Subject)
                    .filter(
                        Subject.name
                        == row["subject"].strip(),
                        Subject.exam_id
                        == exam.id,
                    )
                    .first()
                )

                if subject is None:
                    errors.append(
                        ImportErrorItem(
                            row=index,
                            message=(
                                f"Subject "
                                f"'{row['subject']}' "
                                f"not found."
                            ),
                        )
                    )
                    continue

                # ------------------------------------------
                # Find Topic
                # ------------------------------------------

                topic = (
                    db.query(Topic)
                    .filter(
                        Topic.name
                        == row["topic"].strip(),
                        Topic.subject_id
                        == subject.id,
                    )
                    .first()
                )

                if topic is None:
                    errors.append(
                        ImportErrorItem(
                            row=index,
                            message=(
                                f"Topic "
                                f"'{row['topic']}' "
                                f"not found."
                            ),
                        )
                    )
                    continue

                # ------------------------------------------
                # Duplicate question
                # ------------------------------------------

                duplicate = (
                    db.query(Question)
                    .filter(
                        Question.question_text
                        == row[
                            "question_text"
                        ].strip(),
                        Question.topic_id
                        == topic.id,
                    )
                    .first()
                )

                if duplicate is not None:
                    duplicates += 1
                    continue

                # ------------------------------------------
                # Create question
                # ------------------------------------------

                question = Question(
                    topic_id=topic.id,
                    question_text=row[
                        "question_text"
                    ].strip(),
                    explanation=(
                        row.get(
                            "explanation",
                            "",
                        ).strip()
                        or None
                    ),
                    marks=float(
                        row.get(
                            "marks",
                            2.0,
                        )
                        or 2.0
                    ),
                    negative_marks=float(
                        row.get(
                            "negative_marks",
                            0.0,
                        )
                        or 0.0
                    ),
                    difficulty=(
                        row.get(
                            "difficulty",
                            "Medium",
                        ).strip()
                        or "Medium"
                    ),
                    question_type=(
                        row.get(
                            "question_type",
                            "MCQ_SINGLE",
                        ).strip()
                        or "MCQ_SINGLE"
                    ),
                    exam_stage=(
                        row.get(
                            "exam_stage",
                            "Prelims",
                        ).strip()
                        or "Prelims"
                    ),
                    estimated_time=int(
                        row.get(
                            "estimated_time",
                            60,
                        )
                        or 60
                    ),
                    language=(
                        row.get(
                            "language",
                            "English",
                        ).strip()
                        or "English"
                    ),
                    year=(
                        int(row["year"])
                        if row.get("year")
                        else None
                    ),
                    source=(
                        row.get(
                            "source",
                            "",
                        ).strip()
                        or None
                    ),
                    is_pyq=(
                        str(
                            row.get(
                                "is_pyq",
                                "false",
                            )
                        )
                        .strip()
                        .lower()
                        == "true"
                    ),
                    is_active=True,
                )

                db.add(question)

                # Get question ID
                db.flush()

                # ------------------------------------------
                # Create options
                # ------------------------------------------

                option_columns = [
                    ("option_a", 1),
                    ("option_b", 2),
                    ("option_c", 3),
                    ("option_d", 4),
                ]

                correct_option = (
                    row[
                        "correct_option"
                    ]
                    .strip()
                    .upper()
                )

                for column_name, display_order in (
                    option_columns
                ):

                    option_text = (
                        row.get(
                            column_name,
                            "",
                        ).strip()
                    )

                    if not option_text:
                        continue

                    option_letter = (
                        column_name[-1].upper()
                    )

                    db.add(
                        QuestionOption(
                            question_id=question.id,
                            option_text=option_text,
                            display_order=display_order,
                            is_correct=(
                                option_letter
                                == correct_option
                            ),
                        )
                    )

                # Commit this successful row
                db.commit()

                imported += 1

            except Exception as exc:

                # Roll back only the current row
                db.rollback()

                errors.append(
                    ImportErrorItem(
                        row=index,
                        message=(
                            f"Import failed: "
                            f"{str(exc)}"
                        ),
                    )
                )

        # --------------------------------------------------
        # Final response
        # --------------------------------------------------

        return ImportResponse(
            success=(
                len(errors) == 0
            ),
            summary=ImportSummary(
                total_rows=len(rows),
                imported=imported,
                duplicates=duplicates,
                failed=len(errors),
            ),
            errors=errors,
        )