from djongo import models

from ..question import Question

class QuestionItem(models.Model):
    question_id = models.CharField(max_length=12)
    next_question_id = models.CharField(max_length=12)
    prev_question_id = models.CharField(max_length=12)

    def __str__(self):
        return Question.objects.get(id=self.question_id)
