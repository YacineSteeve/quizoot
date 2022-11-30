from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("quizzes/", view=views.quiz_list, name="quizzes-list"),
    path("questions/", view=views.question_list, name="questions-list"),
]
