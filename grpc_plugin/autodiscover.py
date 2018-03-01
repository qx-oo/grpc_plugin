import inspect
from .decorators import BaseGrpc
import os
import grpc_plugin.proto
import importlib


def autodiscover_grpc(installed_apps):
    """
    Discover app grpc class
    """
    grpc_cls_list = []
    for app in installed_apps:
        module = importlib.import_module('.'.join([app, 'grpc_view']))
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if issubclass(obj, BaseGrpc):
                    grpc_cls_list.append(obj)
    return grpc_cls_list


def autodiscover_grpc_service():
    """
    """
    file_list = os.listdir(grpc_plugin.proto.__path__[0])
    grpc_list = [fl[:-3] for fl in file_list if fl.endswith('grpc.py')]
    for grpc_f in grpc_list:
        inspect.getmembers('grpc_plugin.proto.%s' % grpc_f)
