from djongo import models

from ..question import Question
from .. import utils


class QuestionItem(models.Model):
    question_id = models.CharField(
        max_length=utils.ID_LENGTH, help_text="Id of a question referenced in the quiz."
    )
    next_question_id = models.CharField(
        max_length=utils.ID_LENGTH,
        null=True,
        blank=True,
        help_text="Id of the next question in the quiz chronology. (Keep empty if None)",
    )
    prev_question_id = models.CharField(
        max_length=utils.ID_LENGTH,
        null=True,
        blank=True,
        help_text="Id of the previous question in the quiz chronology. (Keep empty if None)",
    )

    class Meta:
        verbose_name_plural = "  Question items"

    def save(self, *args, **kwargs):
        if self.next_question_id == "":
            self.next_question_id = None
        if self.prev_question_id == "":
            self.prev_question_id = None

        existing_question_ids = Question.objects.values_list("id", flat=True).distinct()

        for id_field in [
            self.question_id,
            self.next_question_id,
            self.prev_question_id,
        ]:
            utils.validate_id(id_field, existing_question_ids, "question")

        super().save(*args, **kwargs)

    def __str__(self):
        return Question.objects.get(id=self.question_id)
