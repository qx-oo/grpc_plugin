from django.core.management import BaseCommand
from django.conf import settings
import logging
from grpc_plugin.autodiscover import (
    autodiscover_grpc,
    autodiscover_grpc_service,
    )
from concurrent import futures
import grpc
import time


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Command(BaseCommand):
    def handle(self, **options):
        """

        """
        installed_apps = settings.INSTALLED_APPS

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        service_data = autodiscover_grpc_service()
        for cls in autodiscover_grpc(installed_apps):
            for _, data in service_data.items():
                if not data.get('class') or not data.get('server'):
                    continue
                if issubclass(cls, data.get('class')):
                    data.get('server')(cls(), server)
        server.add_insecure_port("[::]:50051")
        server.start()

        print('start grpc server: [::]:50051')

        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)
