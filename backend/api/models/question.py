from djongo import models

from .submodels.question_spec import QuestionSpec
from .submodels.grading import Grading
from .submodels.types import Tag
from . import utils


class Question(models.Model):
    DIFFICULTIES = [("EASY", "Easy"), ("MEDIUM", "Medium"), ("HARD", "Hard")]

    QUESTION_KIND = [
        ("CHOICE_QUESTION", "Choice Question"),
        ("TEXT_QUESTION", "Text Question"),
        ("UPLOAD_QUESTION", "Upload Question"),
        ("CODE_QUESTION", "Code Question"),
    ]

    id = models.CharField(
        max_length=utils.ID_LENGTH,
        primary_key=True,
        editable=False,
        help_text="Id of the question.",
    )
    question = models.CharField(
        max_length=500,
        unique=True,
        help_text="The actual question as a human-readable string.",
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTIES,
        default="EASY",
        help_text="Rate how difficult the question is.",
    )
    kind = models.CharField(
        max_length=25,
        choices=QUESTION_KIND,
        default="CHOICE_QUESTION",
        help_text="The question kind.",
    )
    spec = models.OneToOneField(
        QuestionSpec,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Spec of the question. It specifies what the attributes of the question are.",
    )
    grading = models.EmbeddedField(
        model_container=Grading,
        help_text="Specifies how to grade for the current question.",
    )
    tags = models.ArrayReferenceField(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="List of optional tags associated with the question.",
    )
    hint = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Hint given to help answering the question.",
    )

    class Meta:
        verbose_name_plural = "     Questions"

    def save(self, *args, **kwargs):
        self.id = utils.generate_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question} ({self.difficulty})"
