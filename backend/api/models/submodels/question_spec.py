from djongo import models

from .question_option import QuestionOption
from .types import File, OptionId


class ChoiceQuestion(models.Model):
    options = models.ArrayReferenceField(QuestionOption)

    def __str__(self):
        return


class SingleChoiceQuestion(ChoiceQuestion):
    answer_id = models.OneToOneField(OptionId, on_delete=models.CASCADE, related_name="answer_id")

    class Meta:
        abstract = True


class MultipleChoicesQuestion(ChoiceQuestion):
    answers_id = models.ArrayReferenceField(OptionId)

    class Meta:
        abstract = True


class TextQuestion(models.Model):
    keywords = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return


class UploadQuestion(models.Model):
    files = models.ArrayReferenceField(File)
    max_size = models.CharField(max_length=10)
    max_files = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return


class CodeQuestion(models.Model):
    content = models.TextField()
    language = models.CharField(max_length=25, default="python3")
    expected_output = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return


class QuestionSpec(SingleChoiceQuestion,
                   MultipleChoicesQuestion,
                   TextQuestion,
                   UploadQuestion,
                   CodeQuestion):

    def __str__(self):
        return
