from django.contrib import admin

from .models.submodels.choice_question_option import ChoiceQuestionOption
from .models.submodels.question_item import QuestionItem
from .models.submodels.question_spec import QuestionSpec
from .models.submodels.author import Author
from .models.submodels.types import File, Tag, OptionId
from .models import Quiz, Question

admin.site.register(File)
admin.site.register(Tag)
admin.site.register(OptionId)
admin.site.register(ChoiceQuestionOption)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Author)
admin.site.register(QuestionItem)


@admin.register(QuestionSpec)
class QuestionSpecAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Choice Question", {"fields": ("options", "answer_id", "answers_id")}),
        ("Text Question", {"fields": ("keywords",)}),
        ("Upload Question", {"fields": ("files", "max_size", "max_files")}),
        ("Code Question", {"fields": ("content", "language", "expected_output")}),
    )
