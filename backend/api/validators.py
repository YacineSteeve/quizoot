import json
from typing import Any, Literal

import jsonschema
from django.conf import settings


class InvalidData(Exception):
    pass


class InvalidCollection(Exception):
    pass


class SchemaValidator:
    __schema_dir = settings.BASE_DIR / "schemas"

    def __init__(self) -> None:
        self._quiz_schema = None
        self._question_schema = None

        with open(self.__schema_dir / "quiz.json") as file:
            self._quiz_schema = json.load(file)

        with open(self.__schema_dir / "question.json") as file:
            self._schema = json.load(file)

    def validate(self, data: Any, collection: Literal["quizzes", "questions"]) -> None:
        try:
            if collection == "quizzes":
                jsonschema.validate(data, self._quiz_schema)
            elif collection == "questions":
                jsonschema.validate(data, self._question_schema)
            else:
                raise InvalidCollection(
                    "Collection must be literal 'quiz' or 'question'"
                )
        except jsonschema.exceptions.ValidationError as err:
            raise InvalidData(err.message)
