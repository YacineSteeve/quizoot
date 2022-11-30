from rest_framework.decorators import api_view

from ..client import client
from ..utils import JsonResponse


@api_view(["GET"])
def quiz_list(request):
    if request.method == "GET":
        return JsonResponse(data=client.collection("quizzes").find())
