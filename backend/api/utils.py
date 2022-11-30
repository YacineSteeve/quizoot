import json
from bson import json_util
from typing import Any

from rest_framework.response import Response


class ApiResponse(Response):
    def __init__(self, data: Any, *args, **kwargs):
        super().__init__(json.loads(json_util.dumps(data)), *args, **kwargs)
