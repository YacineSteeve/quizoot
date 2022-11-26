from djongo import models

from .submodels.question_item import QuestionItem
from .submodels.author import Author
from .submodels.types import Tag


class Quiz(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    title = models.CharField(max_length=40)
    description = models.TextField()
    max_score = models.IntegerField(default=0)
    questions = models.ArrayReferenceField(QuestionItem)
    authors = models.ArrayReferenceField(Author)
    tags = models.ArrayReferenceField(Tag)

    class Meta:
        verbose_name_plural = "quizzes"

    def __str__(self):
        return str(self.title)
