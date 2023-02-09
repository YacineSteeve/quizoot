from django.http import Http404
from pymongo.collection import ReturnDocument
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView

from ..client import client
from ..exceptions import InvalidData
from ..utils import JsonResponse, get_new_id, get_sort_order
from ..validators import SchemaValidator


class QuestionApiView(APIView):
    _questions = client.collection("questions")
    _validator = SchemaValidator("questions")


class QuestionList(QuestionApiView):
    """LIST all questions and CREATE new question."""

    def get(self, request: Request):
        sort_order = get_sort_order(request.query_params, self._questions)
        return JsonResponse(data=self._questions.find(sort=sort_order))

    def post(self, request: Request):
        question_data = request.data
        question_data["id"] = get_new_id()

        try:
            self._validator.validate(question_data)
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            insertion_result = self._questions.insert_one(question_data)
            inserted_question = self._questions.find_one(
                {"_id": insertion_result.inserted_id}
            )
            return JsonResponse(data=inserted_question, status=status.HTTP_201_CREATED)


class QuestionDetail(QuestionApiView):
    """GET, PATCH and DELETE a single question."""

    def get(self, request: Request, pk: str):
        question = self._questions.find_one({"id": pk})

        if question is None:
            raise Http404("There is no question matching your query.")
        else:
            return JsonResponse(data=question)

    def patch(self, request: Request, pk: str) -> JsonResponse:
        question_data = request.data

        try:
            self._validator.validate(question_data)
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            updated_question = self._questions.find_one_and_update(
                {"id": pk},
                {"$set": question_data},
                # Return the updated document
                return_document=ReturnDocument.AFTER,
            )
            return JsonResponse(data=updated_question)

    def delete(self, request: Request, pk: str) -> JsonResponse:
        self._questions.find_one_and_delete({"id": pk})
        # A JSON with the deleted item id is returned, as to confirm deletion
        return JsonResponse(data={"id": pk})
