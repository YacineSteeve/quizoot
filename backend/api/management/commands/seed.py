import json
from argparse import ArgumentParser
from pathlib import PosixPath

from django.conf import settings
from django.core.management.base import BaseCommand

from backend.api.client import CollectionName, client

# USAGE :
#   python manage.py seed

MODE_CLEAR = "clear"
MODE_REFRESH = "refresh"


DATA_DIR: PosixPath = settings.BASE_DIR / "data"


# TODO: add a logger ?
class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        # Always clear data
        self.clear_data()
        for filepath in DATA_DIR.glob("*.json"):
            collection_name = filepath.name[:-5]
            self.seed_data(collection_name)

    def clear_data(self):
        self.stdout.write("[INFO] Deleting all collections...")
        for name in client._collections:
            result = client.collection(name).delete_many({})
            self.stdout.write(
                '[INFO] Deleted %s documents from "%s"' % (result.deleted_count, name)
            )

    def seed_data(self, collection_name: CollectionName):
        self.stdout.write('[INFO] seeding data in collection "%s"' % collection_name)
        data = self._read_json_data(collection_name)
        collection = client.collection(collection_name)
        try:
            collection.insert_many(data)
            self.stdout.write(
                "[INFO] \t --> %s documents inserted" % collection.count_documents({})
            )
        except Exception as err:
            self.stderr.write(
                '[ERROR] Unable to seed data from "%s/%s.json" to collection %s\n'
                % (DATA_DIR, collection_name, collection_name)
            )
            self.stderr.write(err)

    def _read_json_data(self, filename: str):
        with open(DATA_DIR / f"{filename}.json") as file:
            return json.load(file)
