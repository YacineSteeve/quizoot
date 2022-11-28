from rest_framework.decorators import api_view

from ..config import client
from ..utils import ApiResponse

@api_view(['GET'])
def quiz_list(request):
    if request.method == "GET":
        return ApiResponse(data=client.collection("quizzes").find())
