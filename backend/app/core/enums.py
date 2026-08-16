from enum import Enum


class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class QuestionType(str, Enum):
    MCQ_SINGLE = "MCQ_SINGLE"
    MCQ_MULTIPLE = "MCQ_MULTIPLE"
    TRUE_FALSE = "TRUE_FALSE"
    ASSERTION_REASON = "ASSERTION_REASON"
    MATCH_THE_FOLLOWING = "MATCH_THE_FOLLOWING"
    PASSAGE_BASED = "PASSAGE_BASED"
    IMAGE_BASED = "IMAGE_BASED"
    NUMERICAL = "NUMERICAL"


class ExamStage(str, Enum):
    PRELIMS = "Prelims"
    MAINS = "Mains"
    INTERVIEW = "Interview"