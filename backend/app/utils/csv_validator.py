import csv
from io import StringIO


REQUIRED_COLUMNS = [
    "exam",
    "subject",
    "topic",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_option",
]


def validate_csv(file_content: str):
    """
    Validate uploaded question CSV.

    Returns:
        {
            "rows": [...],
            "errors": [...]
        }
    """

    errors = []

    reader = csv.DictReader(
        StringIO(file_content)
    )

    # --------------------------------------------------
    # Validate header
    # --------------------------------------------------

    if reader.fieldnames is None:
        return {
            "rows": [],
            "errors": [
                "CSV file is empty or has no header."
            ],
        }

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in reader.fieldnames
    ]

    if missing_columns:
        return {
            "rows": [],
            "errors": [
                (
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                )
            ],
        }

    rows = []

    # --------------------------------------------------
    # Validate rows
    # --------------------------------------------------

    for row_number, row in enumerate(
        reader,
        start=2,
    ):

        row_has_error = False

        # ----------------------------------------------
        # Question text
        # ----------------------------------------------

        question_text = (
            row.get("question_text", "")
            or ""
        ).strip()

        if not question_text:
            errors.append(
                f"Row {row_number}: "
                "Question text is empty."
            )
            row_has_error = True

        # ----------------------------------------------
        # Options
        # ----------------------------------------------

        for option in [
            "option_a",
            "option_b",
            "option_c",
            "option_d",
        ]:
            option_value = (
                row.get(option, "")
                or ""
            ).strip()

            if not option_value:
                errors.append(
                    f"Row {row_number}: "
                    f"{option} is empty."
                )
                row_has_error = True

        # ----------------------------------------------
        # Correct option
        # ----------------------------------------------

        correct_option = (
            row.get("correct_option", "")
            or ""
        ).strip().upper()

        if correct_option not in [
            "A",
            "B",
            "C",
            "D",
        ]:
            errors.append(
                f"Row {row_number}: "
                f"Invalid correct option "
                f"'{correct_option}'."
            )
            row_has_error = True

        # ----------------------------------------------
        # Exam
        # ----------------------------------------------

        if not (
            row.get("exam", "")
            or ""
        ).strip():
            errors.append(
                f"Row {row_number}: "
                "Exam is empty."
            )
            row_has_error = True

        # ----------------------------------------------
        # Subject
        # ----------------------------------------------

        if not (
            row.get("subject", "")
            or ""
        ).strip():
            errors.append(
                f"Row {row_number}: "
                "Subject is empty."
            )
            row_has_error = True

        # ----------------------------------------------
        # Topic
        # ----------------------------------------------

        if not (
            row.get("topic", "")
            or ""
        ).strip():
            errors.append(
                f"Row {row_number}: "
                "Topic is empty."
            )
            row_has_error = True

        # ----------------------------------------------
        # Optional numeric fields
        # ----------------------------------------------

        marks = (
            row.get("marks", "")
            or ""
        ).strip()

        if marks:
            try:
                marks_value = float(marks)

                if marks_value < 0:
                    errors.append(
                        f"Row {row_number}: "
                        "Marks cannot be negative."
                    )
                    row_has_error = True

            except ValueError:
                errors.append(
                    f"Row {row_number}: "
                    f"Invalid marks '{marks}'."
                )
                row_has_error = True

        negative_marks = (
            row.get("negative_marks", "")
            or ""
        ).strip()

        if negative_marks:
            try:
                negative_value = float(
                    negative_marks
                )

                if negative_value < 0:
                    errors.append(
                        f"Row {row_number}: "
                        "Negative marks cannot "
                        "be negative."
                    )
                    row_has_error = True

            except ValueError:
                errors.append(
                    f"Row {row_number}: "
                    "Invalid negative marks "
                    f"'{negative_marks}'."
                )
                row_has_error = True

        # ----------------------------------------------
        # Estimated time
        # ----------------------------------------------

        estimated_time = (
            row.get("estimated_time", "")
            or ""
        ).strip()

        if estimated_time:
            try:
                time_value = int(
                    estimated_time
                )

                if time_value <= 0:
                    errors.append(
                        f"Row {row_number}: "
                        "Estimated time must "
                        "be greater than 0."
                    )
                    row_has_error = True

            except ValueError:
                errors.append(
                    f"Row {row_number}: "
                    "Invalid estimated time "
                    f"'{estimated_time}'."
                )
                row_has_error = True

        # ----------------------------------------------
        # Year
        # ----------------------------------------------

        year = (
            row.get("year", "")
            or ""
        ).strip()

        if year:
            try:
                int(year)
            except ValueError:
                errors.append(
                    f"Row {row_number}: "
                    f"Invalid year '{year}'."
                )
                row_has_error = True

        # ----------------------------------------------
        # Keep valid rows
        # ----------------------------------------------

        if not row_has_error:
            rows.append(row)

    return {
        "rows": rows,
        "errors": errors,
    }