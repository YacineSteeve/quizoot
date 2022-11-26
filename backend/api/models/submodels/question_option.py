from django.db.models import signals
from djongo import models

from .types import OptionId


class QuestionOption(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    display = models.TextField()

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return
        else:
            OptionId.objects.create(value=str(instance.id))

    def __str__(self):
        return str(self.display)


signals.post_save.connect(QuestionOption.post_create, sender=QuestionOption)
