from typing import Literal

import pymongo
import environ

from .exceptions import InvalidCollection

env = environ.Env()
environ.Env.read_env()


class ApiClient(pymongo.MongoClient):
    DATABASE_URL = env("DATABASE_URL")
    DATABASE_NAME = env("DATABASE_NAME")

    def __init__(self):
        super().__init__(self.DATABASE_URL)

        for collection in ["quizzes", "questions"]:
            if collection not in self._database.list_collection_names():
                _ = self._database[collection]

            self._database[collection].create_index(
                [("id", pymongo.ASCENDING)], unique=True
            )

    @property
    def _database(self):
        return self[self.DATABASE_NAME]

    def collection(self, name: Literal["quizzes", "questions"]):
        if name in self._database.list_collection_names():
            return self._database[name]
        else:
            raise InvalidCollection(
                f"'{name}' is not a valid collection name. "
                f"Must be 'quizzes' or 'questions'."
            )


client = ApiClient()
