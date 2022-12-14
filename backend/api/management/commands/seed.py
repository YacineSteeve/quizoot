from django.core.management.base import BaseCommand
from argparse import ArgumentParser

from api.client import client

# USAGE :
#   python manage.py seed --mode=(refresh | clear)

MODE_CLEAR = "clear"
MODE_REFRESH = "refresh"


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--mode", help="Specify the mode (clear | refresh)")

    def handle(self, *args, **options):
        if options.get("mode") == MODE_CLEAR:
            return self.clear_data()

    def clear_data(self):
        self.stdout.write("Deleting all collections...")
        for name in client._collections:
            client.collection(name).drop()
