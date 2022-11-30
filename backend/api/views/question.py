from rest_framework.decorators import api_view

from ..config import client
from ..utils import JsonResponse


@api_view(["GET"])
def question_list(request):
    if request.method == "GET":
        return JsonResponse(data=client.collection("questions").find())
