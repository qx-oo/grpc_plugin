from django.core.management import BaseCommand
from django.conf import settings
import logging
from grpc_plugin.autodiscover import autodiscover_grpc
from concurrent import futures
import grpc
import time


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Command(BaseCommand):
    def handle(self, **options):
        """

        """
        logging.info('start grpc server:')
        installed_apps = settings.INSTALLED_APPS

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        for cls in autodiscover_grpc(installed_apps):
            pass
            # helloworld_pb2_grpc.add_GreeterServicer_to_server(cls(), server)
        server.add_insecure_port("[::]:50051")
        server.start()

        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)
