from djongo import models

from .types import OptionId
from .. import utils


class ChoiceQuestionOption(models.Model):
    id = models.CharField(
        max_length=utils.ID_LENGTH,
        primary_key=True,
        editable=False,
        help_text="The Id of the option.",
    )
    display = models.TextField(
        help_text="The actual display of the option as a human-readable string."
    )

    class Meta:
        verbose_name_plural = "   Choice question options"

    def save(self, *args, **kwargs):
        self.id = utils.generate_id()
        OptionId.objects.create(value=self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.display)
