from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("quizzes/", view=views.quiz_list, name="quizzes-list"),
    path("quizzes/create/", view=views.quiz_create, name="quiz-create"),
    path("quiz/<str:pk>/", view=views.quiz_details, name="quiz-details"),
    path("quiz/<str:pk>/update/", view=views.quiz_update, name="quiz-update"),
    path("quiz/<str:pk>/delete/", view=views.quiz_delete, name="quiz-delete"),
    path("questions/", view=views.question_list, name="questions-list"),
]
