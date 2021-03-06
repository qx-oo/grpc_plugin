from django.core.management import BaseCommand
from django.conf import settings
from grpc_plugin.autodiscover import (
    autodiscover_grpc,
    autodiscover_grpc_service,
    )
from concurrent import futures
import grpc
import time
from grpc_plugin.key.get_key import (
    server_key,
    server_crt,
)
import logging
import sys
from grpc_plugin.interceptor import RequestInterceptor


log = logging.getLogger()
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] - %(levelname)s %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def close_old_connections(func):
    """检查关闭django不可用连接"""
    from django.db import connections

    def wrapper(*args):
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()
        return func(*args)
    return wrapper


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'addrport', nargs='?',
            help='Optional port number, or ipaddr:port'
        )
        parser.add_argument(
            '--ssl', '-s', action='store_true', dest='ssl',
            help='Runserver with ssl',
        )
        parser.add_argument(
            '--worker', '-w', action='store', dest='workers',
            type=int, default=4, help='Thread workers, default 4 worker',
        )

    def handle(self, **options):
        """

        """
        installed_apps = settings.INSTALLED_APPS

        interceptors = (
            RequestInterceptor(),
        )

        workers = options.get('workers')
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers),
                             interceptors=interceptors)

        service_data = autodiscover_grpc_service(installed_apps)
        for cls in autodiscover_grpc(installed_apps):
            for _, data in service_data.items():
                if not data.get('class') or not data.get('server'):
                    continue
                if issubclass(cls, data.get('class')):
                    log.info('rpc: %s.%s' % (cls.__module__, cls.__name__))
                    # 动态设置rpc function
                    for attr in dir(cls):
                        if not attr.startswith('__') or\
                                not attr.startswith('_'):
                            setattr(cls, attr,
                                    close_old_connections(getattr(cls, attr)))
                    data.get('server')(cls(), server)
        addrport = options.get('addrport')
        addrport = addrport if addrport else '[::]:50051'
        if options.get('ssl'):
            server_credentials = grpc.ssl_server_credentials(
                ((server_key(), server_crt(),),))
            server.add_secure_port(addrport, server_credentials)
        else:
            server.add_insecure_port(addrport)
        server.start()

        log.info('start grpc server: %s' % addrport)

        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)
