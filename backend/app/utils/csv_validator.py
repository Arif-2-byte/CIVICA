import csv
from io import StringIO
from typing import List, Dict

REQUIRED_COLUMNS = [
    "exam",
    "subject",
    "topic",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_answer",
    "explanation",
]


def validate_csv(file_content: str):
    """
    Validates uploaded CSV content.

    Returns:
        {
            "rows": [...],
            "errors": [...]
        }
    """

    errors = []

    reader = csv.DictReader(StringIO(file_content))

    # ----------------------------
    # Validate Header
    # ----------------------------
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in reader.fieldnames
    ]

    if missing_columns:
        return {
            "rows": [],
            "errors": [
                f"Missing required columns: {', '.join(missing_columns)}"
            ],
        }

    rows = []

    for row_number, row in enumerate(reader, start=2):

        # ----------------------------
        # Question cannot be empty
        # ----------------------------
        if not row["question_text"].strip():
            errors.append(
                f"Row {row_number}: Question text is empty."
            )

        # ----------------------------
        # Options cannot be empty
        # ----------------------------
        for option in [
            "option_a",
            "option_b",
            "option_c",
            "option_d",
        ]:
            if not row[option].strip():
                errors.append(
                    f"Row {row_number}: {option} is empty."
                )

        # ----------------------------
        # Correct Answer Validation
        # ----------------------------
        answer = row["correct_answer"].strip().upper()

        if answer not in ["A", "B", "C", "D"]:
            errors.append(
                f"Row {row_number}: Invalid correct answer '{answer}'."
            )

        rows.append(row)

    return {
        "rows": rows,
        "errors": errors,
    }