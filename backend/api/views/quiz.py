from .views import ListView, DetailView

class QuizList(ListView):
    def __init__(self):
        super().__init__('quizzes')


class QuizDetail(DetailView):
    def __init__(self):
        super().__init__('quizzes')
