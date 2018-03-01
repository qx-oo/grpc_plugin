from django.core.management import BaseCommand
from django.conf import settings
import logging


class Command(BaseCommand):
    def handle(self, **options):
        """

        """
        logging.info('auto scan')
        installed_apps = settings.INSTALLED_APPS
        for app in installed_apps:
            pass
