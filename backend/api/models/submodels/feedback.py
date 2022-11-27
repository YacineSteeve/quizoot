from djongo import models


class FeedbackAbstract(models.Model):
    explanation = models.TextField(
        null=True,
        blank=True,
        help_text="General feedback/explanation displayed whether the answer is wrong or correct.",
    )
    when_wrong = models.TextField(
        null=True, blank=True, help_text="Feedback when answer is wrong."
    )
    when_right = models.TextField(
        null=True, blank=True, help_text="Feedback when answer is right."
    )

    class Meta:
        abstract = True


class Feedback(FeedbackAbstract):
    _id = models.ObjectIdField()
