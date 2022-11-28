from djongo import models

from .choice_question_option import ChoiceQuestionOption
from .types import File, OptionId


class BaseQuestionSpec(models.Model):
    class Meta:
        abstract = True


class ChoiceQuestion(BaseQuestionSpec):
    options = models.ArrayReferenceField(
        ChoiceQuestionOption, null=True, blank=True, help_text="The question options."
    )

    class Meta:
        abstract = True


class SingleChoiceQuestion(ChoiceQuestion):
    answer_id = models.ForeignKey(
        OptionId,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="answer_id",
        help_text="Id of the correct answer to the question (if single choice).",
    )

    class Meta:
        abstract = True


class MultipleChoicesQuestion(ChoiceQuestion):
    answers_id = models.ArrayReferenceField(
        OptionId,
        null=True,
        blank=True,
        help_text="Id of the correct answers to the question (if multiple choices).",
    )

    class Meta:
        abstract = True


class TextQuestion(BaseQuestionSpec):
    keywords = models.TextField(
        null=True,
        blank=True,
        help_text="List of keywords that the answers should contain.",
    )

    class Meta:
        abstract = True


class UploadQuestion(BaseQuestionSpec):
    files = models.ArrayReferenceField(
        File, null=True, blank=True, help_text="List of files to upload."
    )
    max_size = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Maximum size of each files. Can be expressed in bytes, megabytes (MB), etc.",
    )
    max_files = models.IntegerField(
        default=1, null=True, blank=True, help_text="Maximum number of files to upload."
    )

    class Meta:
        abstract = True


class CodeQuestion(BaseQuestionSpec):
    content = models.TextField(
        null=True,
        blank=True,
        help_text="Code content. This will be run using a `python3` runner and evaluated.",
    )
    language = models.CharField(
        max_length=25,
        default="python3",
        null=True,
        blank=True,
        help_text="Coding language. Only `python3` is supported.",
    )
    expected_output = models.TextField(
        null=True, blank=True, help_text="Expected output after running the code."
    )

    class Meta:
        abstract = True


class QuestionSpec(
    SingleChoiceQuestion,
    MultipleChoicesQuestion,
    TextQuestion,
    UploadQuestion,
    CodeQuestion,
):
    _id = models.ObjectIdField()

    class Meta:
        verbose_name_plural = "    Question specs"

    def __str__(self):
        return str(self.language)
