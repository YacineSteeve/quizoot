import json
from typing import Any
from inflector import Inflector

import pymongo
from bson import ObjectId, json_util
from django.http.request import QueryDict
from pymongo.collection import Collection
from rest_framework.response import Response

DEFAULT_SORT_KEY = "id"

DEFAULT_SORT_ORDER = pymongo.ASCENDING

SORT_ORDER = {
    "ascending": pymongo.ASCENDING,
    "descending": pymongo.DESCENDING,
}


class StringUtils:
    _inflector = Inflector()

    @classmethod
    def singularize(cls, word: str) -> str:
        return cls._inflector.singularize(word)

    @classmethod
    def pluralize(cls, word: str) -> str:
        return cls._inflector.pluralize(word)


def _to_python_object(obj: Any) -> Any:
    return json.loads(json_util.dumps(obj))


class JsonResponse(Response):
    def __init__(self, data: Any, *args, **kwargs):
        super().__init__(_to_python_object(data), *args, **kwargs)


def get_sort_order(query_params: QueryDict, collection: Collection):
    sort_key = query_params.get("sort_key", DEFAULT_SORT_KEY)
    sort_key = str(sort_key).lower()
    # TODO: Find a way to check if the sort_key in a valid key of the `collection`.

    sort_order = query_params.get("sort_order")
    sort_order = SORT_ORDER.get(str(sort_order).lower(), DEFAULT_SORT_ORDER)

    return [(sort_key, sort_order)]


def get_new_id() -> str:
    return str(ObjectId())
