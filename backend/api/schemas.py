import json
from pathlib import PosixPath
from typing import Any

import jsonschema
from django.conf import settings

from .exceptions import InvalidData


class SchemaLoader:
    _schema_dir: PosixPath = settings.BASE_DIR / "interfaces/schemas"
    _schemas = set()
    _cache = {}

    def __init__(self):
        self.reload()

    def load(self, schema_name: str):
        if not schema_name.endswith(".json"):
            schema_name += ".json"
        if schema_name not in self._schemas:
            raise Exception(
                "'%s' does not exists in folder '%s'. Consider reloading your %s instance using the .reload() method"
                % (schema_name, self._schema_dir, self.__class__.__name__)
            )
        if schema_name not in self._cache:
            with open(self._schema_dir / schema_name) as file:
                self._cache[schema_name] = json.load(file)
        return self._cache

    def reload(self, invalidate_cache=False):
        for schema in self._schema_dir.glob("*.json"):
            self._schemas.add(schema.name)
        if invalidate_cache is True:
            self._cache = {}


loader = SchemaLoader()


class SchemaValidator:
    def __init__(self, name: str) -> None:
        self._schema = loader.load(name)

    def validate(self, data: Any) -> None:
        try:
            jsonschema.validate(data, self._schema)
        except jsonschema.exceptions.ValidationError as err:
            raise InvalidData(err.message)
