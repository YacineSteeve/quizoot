from djongo import models

from .submodels.question_item import QuestionItem
from .submodels.author import Author
from .submodels.types import Tag
from . import utils


class Quiz(models.Model):
    id = models.CharField(
        max_length=utils.ID_LENGTH,
        primary_key=True,
        editable=False,
        help_text="Id of the quiz.",
    )
    title = models.CharField(
        max_length=40, unique=True, help_text="The title (header) of the quiz."
    )
    description = models.TextField(
        help_text="A brief description of the quiz content, topic..."
    )
    max_score = models.IntegerField(
        default=0, help_text="Maximum score the user can get."
    )
    questions = models.ManyToManyField(
        QuestionItem, help_text="All the questions the quiz is made of."
    )
    authors = models.ArrayReferenceField(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="List of optional authors or contributors of the quiz.",
    )
    tags = models.ArrayReferenceField(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="List of optional tags associated with the quiz.",
    )

    class Meta:
        verbose_name_plural = "      Quizzes"

    def save(self, *args, **kwargs):
        self.id = utils.generate_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
