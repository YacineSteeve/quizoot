from ._generic_views import ListView, DetailView


class QuestionList(ListView):
    def __init__(self):
        super().__init__("questions")


class QuestionDetail(DetailView):
    def __init__(self):
        super().__init__("questions")
