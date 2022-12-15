from django.http import Http404
from pymongo.collection import ReturnDocument
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView

from ..client import client
from ..exceptions import InvalidData
from ..utils import JsonResponse, get_new_id, get_sort_order
from ..validators import SchemaValidator


class QuizApiView(APIView):
    _quizzes = client.collection("quizzes")
    _validator = SchemaValidator("quizzes")


class QuizList(QuizApiView):
    """LIST all quizzes and CREATE new quiz."""

    def get(self, request: Request):
        sort_order = get_sort_order(request.query_params, self._quizzes)
        return JsonResponse(data=self._quizzes.find(sort=sort_order))

    def post(self, request: Request):
        quiz_data = request.data
        quiz_data["id"] = get_new_id()

        try:
            self._validator.validate(quiz_data)
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            insertion_result = self._quizzes.insert_one(quiz_data)
            inserted_quiz = self._quizzes.find_one(
                {"_id": insertion_result.inserted_id}
            )
            return JsonResponse(data=inserted_quiz, status=status.HTTP_201_CREATED)


class QuizDetail(QuizApiView):
    """GET, PATCH and DELETE a single quiz."""

    def get(self, request: Request, pk: str):
        quiz = self._quizzes.find_one({"id": pk})

        if quiz is None:
            raise Http404("There is no quiz matching your query.")
        else:
            return JsonResponse(data=quiz)

    def patch(self, request: Request, pk: str) -> JsonResponse:
        quiz_data = request.data

        try:
            self._validator.validate(quiz_data)
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            updated_quiz = self._quizzes.find_one_and_update(
                {"id": pk},
                {"$set": quiz_data},
                # Return the updated document
                return_document=ReturnDocument.AFTER,
            )
            return JsonResponse(data=updated_quiz)

    def delete(self, request: Request, pk: str) -> JsonResponse:
        self._quizzes.find_one_and_delete({"id": pk})
        # A JSON with the deleted item id is returned, as to confirm deletion
        return JsonResponse(data={"id": pk})
