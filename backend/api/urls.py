from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("quizzes/", view=views.QuizList.as_view(), name="quizzes-list"),
    path("quizzes/<str:pk>/", view=views.QuizDetail.as_view(), name="quiz-details"),
    path("questions/", view=views.QuestionList.as_view(), name="questions-list"),
    path(
        "questions/<str:pk>/",
        view=views.QuestionDetail.as_view(),
        name="question-details",
    ),
]
