import json
from typing import Any, Literal

import jsonschema
from django.conf import settings

from .exceptions import InvalidData, InvalidCollection


class SchemaValidator:
    __schemas_base_dir = settings.BASE_DIR / "interfaces/schemas"
    __schemas = {"quizzes": "quiz.json", "questions": "question.json"}

    def __init__(self, collection: Literal["quizzes", "questions"]) -> None:
        if collection not in self.__schemas:
            raise InvalidCollection("Collection must be literal 'quizzes' or 'questions")

        schema_path = self.__schemas_base_dir / self.__schemas[collection]

        with schema_path.open() as file:
            self._schema = json.load(file)

    def validate(self, data: Any) -> None:
        try:
            jsonschema.validate(data, self._schema)
        except jsonschema.exceptions.ValidationError as err:
            raise InvalidData(err.message)
