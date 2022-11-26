from djongo import models

from .submodels.question_spec import QuestionSpec
from .submodels.grading import Grading
from .submodels.types import Tag

class Question(models.Model):
    DIFFICULTIES = [
        ("EASY", "Easy"),
        ("MEDIUM", "Medium"),
        ("HARD", "Hard")
    ]

    QUESTION_KIND = [
        ("CHOICE_QUESTION", "Choice Question"),
        ("TEXT_QUESTION", "Text Question"),
        ("UPLOAD_QUESTION", "Upload Question"),
        ("CODE_QUESTION", "Code Question"),
    ]

    id = models.CharField(max_length=12, primary_key=True)
    question = models.CharField(max_length=12)
    kind = models.CharField(max_length=20, choices=QUESTION_KIND, default="CHOICE_QUESTION")
    spec = models.OneToOneField(QuestionSpec, on_delete=models.CASCADE)
    grading = models.OneToOneField(Grading, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTIES, default="EASY")
    tags = models.ArrayReferenceField(Tag)
    hint = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.question} ({self.difficulty})"
