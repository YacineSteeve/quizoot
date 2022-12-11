import json
from bson import json_util
from typing import Any, List, Tuple, Type

import pymongo
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response

from .exceptions import CollectionFull


__Collection = type(Type[pymongo.collection.Collection])

MIN_ID_VALUE = 100_000_000_000
MAX_ID_VALUE = 999_999_999_999
DEFAULT_QUERY_LIST_SORT_KEY = "id"
DEFAULT_QUERY_LIST_SORT_ORDER = pymongo.ASCENDING
QUERY_LIST_SORT_ORDER = {
    "ascending": pymongo.ASCENDING,
    "descending": pymongo.DESCENDING,
}


def _to_python_object(obj: Any) -> Any:
    return json.loads(json_util.dumps(obj))


class JsonResponse(Response):
    def __init__(self, data: Any, *args, **kwargs):
        super().__init__(_to_python_object(data), *args, **kwargs)


def get_sort_order_from_request(
    request: WSGIRequest, collection: __Collection
) -> List[Tuple[str, int]]:

    sort_key: Any = request.query_params.get("sort_key", None)
    sort_order: Any = request.query_params.get("sort_order", None)

    if sort_key is None:
        sort_key = DEFAULT_QUERY_LIST_SORT_KEY
    else:
        sort_key = str(sort_key).lower()
        # TODO: Find a way to check if the sort_key in a valid key of the `collection`.

    if sort_order is None:
        sort_order = DEFAULT_QUERY_LIST_SORT_ORDER
    else:
        sort_order = QUERY_LIST_SORT_ORDER.get(
            str(sort_order).lower(), DEFAULT_QUERY_LIST_SORT_ORDER
        )

    return [(sort_key, sort_order)]


def get_new_id(collection: __Collection) -> str:
    if collection.find_one() is None:
        return str(MIN_ID_VALUE)
    else:
        current_max_id = _to_python_object(
            collection.find().sort("id", pymongo.DESCENDING).limit(1)
        )[0]["id"]

        if int(current_max_id) < MAX_ID_VALUE:
            return str(int(current_max_id) + 1)
        else:
            raise CollectionFull(
                f"The {collection.name} is full! You can't create a new object."
            )
