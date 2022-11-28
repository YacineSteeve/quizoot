from djongo import models

from .feedback import Feedback


class GradingAbstract(models.Model):
    point_value = models.IntegerField(
        help_text="Specifies how much a correct answer count for in the total score."
    )
    # Feedback
    feedback = models.ArrayField(
        model_container=Feedback,
        help_text="Feedback given after answering the question.",
    )

    class Meta:
        abstract = True


class Grading(GradingAbstract):
    _id = models.ObjectIdField()
