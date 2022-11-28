import pymongo
from django.conf import settings


class ApiClient(pymongo.MongoClient):
    DATABASE_URL = settings.ENV("DATABASE_URL")
    DATABASE_NAME = settings.ENV("DATABASE_NAME")

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

    def collection(self, name: str):
        if name in self._database.list_collection_names():
            return self._database[name]
        else:
            raise ValueError()


client = ApiClient()
