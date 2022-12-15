from typing import List, Literal

import environ
import pymongo
from pymongo.database import Database, Collection

from .exceptions import InvalidCollection

env = environ.Env()
environ.Env.read_env()

CollectionName = Literal["quizzes", "questions"]


class ApiClient(pymongo.MongoClient):
    # Database info from .env
    DATABASE_URL = env("DATABASE_URL")
    DATABASE_NAME = env("DATABASE_NAME")

    # Valid collections
    _collections: List[CollectionName] = ["quizzes", "questions"]

    def __init__(self):
        super().__init__(self.DATABASE_URL)

        for collection in self._collections:
            if collection not in self._database.list_collection_names():
                _ = self._database[collection]

            self._database[collection].create_index(
                [("id", pymongo.ASCENDING)], unique=True
            )

    @property
    def _database(self) -> Database:
        return Database(self, self.DATABASE_NAME)

    def collection(self, name: CollectionName) -> Collection:
        if name in self._database.list_collection_names():
            return self._database[name]
        else:
            raise InvalidCollection(
                f"'{name}' is not a valid collection name. "
                f"Must be 'quizzes' or 'questions'."
            )


client = ApiClient()
