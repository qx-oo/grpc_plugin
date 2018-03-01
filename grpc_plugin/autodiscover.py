import inspect
from .decorators import BaseGrpc


def autodiscover_grpc(installed_apps):
    """
    Discover app grpc class
    """
    grpc_cls_list = []
    for app in installed_apps:
        for name, obj in inspect.getmembers('.'.join([app, 'grpc_view'])):
            if inspect.isclass(obj):
                if issubclass(obj, BaseGrpc):
                    grpc_cls_list.append(obj)
    return grpc_cls_list
