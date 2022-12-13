from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("quizzes/", view=views.QuizList.as_view(), name="quizzes-list"),
    path("quizzes/<str:pk>/", view=views.QuizDetails.as_view(), name="quiz-details"),
    path("questions/", view=views.question_list, name="questions-list"),
]
