from django.http import Http404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from pymongo.collection import ReturnDocument

from ..validators import SchemaValidator
from ..client import client
from ..utils import JsonResponse, get_sort_order_from_request, get_new_id
from ..exceptions import InvalidData


class QuizList(APIView):
    __quizzes = client.collection("quizzes")
    __validator = SchemaValidator("quizzes")

    def get(self, request: Request) -> JsonResponse:
        sort_order = get_sort_order_from_request(request, self.__quizzes)
        return JsonResponse(data=self.__quizzes.find(sort=sort_order))

    def post(self, request: Request) -> JsonResponse:
        quiz_data = request.data
        quiz_data["id"] = get_new_id(self.__quizzes)

        try:
            self.__validator.validate(quiz_data)
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            insertion_result = self.__quizzes.insert_one(quiz_data)
            inserted_quiz = self.__quizzes.find_one(
                {"_id": insertion_result.inserted_id}
            )
            return JsonResponse(data=inserted_quiz, status=status.HTTP_201_CREATED)


class QuizDetails(APIView):
    __quizzes = client.collection("quizzes")
    __validator = SchemaValidator("quizzes")

    def get(self, request: Request, pk: str) -> JsonResponse:
        if request.method == "GET":
            quiz = self.__quizzes.find_one({"id": pk})

            if quiz is None:
                raise Http404("There is no quiz matching your query.")
            else:
                return JsonResponse(data=quiz)

    def patch(self, request: Request, pk: str) -> JsonResponse:
        if request.method == "PATCH":
            quiz_data = request.data

            try:
                self.__validator.validate(quiz_data)
            except InvalidData as error:
                return JsonResponse(
                    data={"message": f"Invalid JSON: {str(error)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                updated_quiz = self.__quizzes.find_one_and_update(
                    {"id": pk},
                    {"$set": quiz_data},
                    # If the document is not already in collection, insert it
                    upsert=True,
                    # Return the updated document
                    return_document=ReturnDocument.AFTER,
                )
                return JsonResponse(data=updated_quiz)

    def delete(self, request: Request, pk: str) -> JsonResponse:
        if request.method == "DELETE":
            self.__quizzes.find_one_and_delete({"id": pk})
            return JsonResponse(
                data={}
            )  # An empty JSON is returned, as to confirm deletion
