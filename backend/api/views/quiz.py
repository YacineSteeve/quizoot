import json

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from pymongo.collection import ReturnDocument

from ..validators import SchemaValidator
from ..client import client
from ..utils import JsonResponse, get_sort_order_from_request, get_new_id
from ..exceptions import InvalidData


__quizzes_collection = client.collection("quizzes")
__quiz_validator = SchemaValidator()


@api_view(["GET"])
def quiz_list(request) -> JsonResponse:
    if request.method == "GET":
        sort_order = get_sort_order_from_request(request, __quizzes_collection)
        return JsonResponse(data=__quizzes_collection.find(sort=sort_order))


@api_view(["GET", "POST"])
def quiz_create(request) -> JsonResponse:
    if request.method == "GET":
        with open(settings.BASE_DIR / "interfaces/schemas/quiz.json") as file:
            quiz_schema = json.loads(file.read())
            # Display the schema on the create view as a template
            return JsonResponse(data=quiz_schema)

    elif request.method == "POST":
        quiz_data = request.data
        quiz_data["id"] = get_new_id(__quizzes_collection)

        try:
            __quiz_validator.validate(quiz_data, "quizzes")
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            insertion_result = __quizzes_collection.insert_one(quiz_data)
            inserted_quiz = __quizzes_collection.find_one(
                {"_id": insertion_result.inserted_id}
            )
            return JsonResponse(data=inserted_quiz, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def quiz_details(request, pk: str) -> JsonResponse:
    if request.method == "GET":
        quiz = __quizzes_collection.find_one({"id": pk})

        if quiz is None:
            return JsonResponse(
                data={"message": "There is no quiz matching your query."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            return JsonResponse(data=quiz)


@api_view(["GET", "POST"])
def quiz_update(request, pk: str) -> JsonResponse:
    if request.method == "GET":
        quiz_to_update = __quizzes_collection.find_one({"id": pk})
        return JsonResponse(data=quiz_to_update)

    elif request.method == "POST":
        quiz_data = request.data

        try:
            __quiz_validator.validate(quiz_data, "quizzes")
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            updated_quiz = __quizzes_collection.find_one_and_update(
                {"id": pk},
                {"$set": quiz_data},
                # If the document is not already in collection, insert it
                upsert=True,
                # Return the updated document
                return_document=ReturnDocument.AFTER,
            )
            return JsonResponse(data=updated_quiz)


@api_view(["GET", "DELETE"])
def quiz_delete(request, pk: str) -> JsonResponse:
    quiz_to_delete = __quizzes_collection.find_one({"id": pk})

    if quiz_to_delete is None:
        return JsonResponse(
            data={"message": "There is no quiz matching your query."},
            status=status.HTTP_404_NOT_FOUND,
        )
    else:
        if request.method == "GET":
            return JsonResponse(data=quiz_to_delete)
        elif request.method == "DELETE":
            __quizzes_collection.find_one_and_delete({"id": pk})
            return JsonResponse(
                data={}
            )  # An empty JSON is returned, as to confirm deletion
