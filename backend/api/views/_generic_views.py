from django.http import Http404
from pymongo.collection import ReturnDocument
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView

from ..client import client, CollectionName
from ..exceptions import InvalidData
from ..utils import JsonResponse, get_new_id, get_sort_order, StringUtils
from ..schemas import SchemaValidator


class GenericApiView(APIView):
    def __init__(self, collection_name: CollectionName):
        super().__init__()
        self._collection = client.collection(collection_name)
        self._validator = SchemaValidator(StringUtils.singularize(collection_name))


class ListView(GenericApiView):
    """LIST all documents and CREATE new document."""

    def __init__(self, collection_name: CollectionName):
        super().__init__(collection_name)

    def get(self, request: Request):
        sort_order = get_sort_order(request.query_params, self._collection)
        documents = []

        for document in self._collection.find(sort=sort_order):
            document.pop("_id", None)
            documents.append(document)

        return JsonResponse(data=documents)

    def post(self, request: Request):
        data = request.data
        data["id"] = get_new_id()

        try:
            self._validator.validate(data)
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            insertion_result = self._collection.insert_one(data)
            inserted_data = self._collection.find_one(
                {"_id": insertion_result.inserted_id}
            )
            return JsonResponse(data=inserted_data, status=status.HTTP_201_CREATED)


class DetailView(GenericApiView):
    """GET, PATCH and DELETE a single document."""

    def __init__(self, collection_name: CollectionName):
        super().__init__(collection_name)

    def get(self, request: Request, pk: str):
        document = self._collection.find_one({"id": pk})

        if document is None:
            raise Http404("There is no document matching your query.")
        else:
            document.pop("_id", None)
            return JsonResponse(data=document)

    def patch(self, request: Request, pk: str) -> JsonResponse:
        data = request.data

        try:
            self._validator.validate(data)
        except InvalidData as error:
            return JsonResponse(
                data={"message": f"Invalid JSON: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            updated_data = self._collection.find_one_and_update(
                {"id": pk},
                {"$set": data},
                # Return the updated document
                return_document=ReturnDocument.AFTER,
            )
            return JsonResponse(data=updated_data)

    def delete(self, request: Request, pk: str) -> JsonResponse:
        self._collection.find_one_and_delete({"id": pk})
        # A JSON with the deleted item id is returned, as to confirm deletion
        return JsonResponse(data={"id": pk})
