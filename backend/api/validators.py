import json
from typing import Any

import jsonschema
from django.conf import settings


class InvalidData(Exception):
    pass


class SchemaValidator:
    __schema_dir = settings.BASE_DIR / "schemas"

    def __init__(self) -> None:
        self._schema = None
        with open(self.__schema_dir / "question.json") as file:
            self._schema = json.load(file)

    def validate(self, data: Any):
        try:
            jsonschema.validate(data, self._schema)
        except jsonschema.exceptions.ValidationError as err:
            raise InvalidData(err.message)
