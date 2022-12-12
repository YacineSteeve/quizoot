import json
from typing import Any, Literal

import jsonschema
from django.conf import settings

from .exceptions import InvalidData, InvalidCollection


class SchemaValidator:
    __schema_dir = settings.BASE_DIR / "interfaces/schemas"
    __schema_names = {
        "quizzes": "quiz.json",
        "questions": "question.json"
    }

    def __init__(self, collection: Literal["quizzes", "questions"]) -> None:
        self._schema = None
        if collection in self.__schema_names.keys():
            with open(self.__schema_dir / self.__schema_names[collection]) as file:
                self._schema = json.load(file)
        else:
            raise InvalidCollection("Collection must be literal 'quizzes' or 'questions")

    def validate(self, data: Any) -> None:
        try:
            jsonschema.validate(data, self._schema)
        except jsonschema.exceptions.ValidationError as err:
            raise InvalidData(err.message)
