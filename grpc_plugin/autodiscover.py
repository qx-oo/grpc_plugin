import inspect
import os
from . import proto
import importlib
import re


def autodiscover_grpc(installed_apps):
    """
    Discover app grpc class
    """
    installed_apps.remove('grpc_plugin')
    grpc_cls_list = []
    for app in installed_apps:
        try:
            module = importlib.import_module('.'.join([app, 'grpc_view']))
        except ModuleNotFoundError:
            continue
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if obj.__module__.startswith('grpc_plugin.proto'):
                    continue
                grpc_cls_list.append(obj)
    return grpc_cls_list


def autodiscover_grpc_service():
    """
    Discover grpc service
    """
    p = re.compile('add_([\w|\d]*)_to_server')

    file_list = os.listdir(proto.__path__[0])
    grpc_list = [fl[:-3] for fl in file_list if fl.endswith('grpc.py')]

    module_data = {}
    for grpc_f in grpc_list:
        module = importlib.import_module('%s.%s' % (proto.__name__,
                                                    grpc_f))

        for name, obj in inspect.getmembers(module):
            add_server = p.findall(name)[:1]
            if name.endswith('Servicer'):
                if not module_data.get(name):
                    module_data[name] = {}
                module_data[name]['class'] = obj
            if add_server:
                if not module_data.get(add_server[0]):
                    module_data[add_server[0]] = {}
                module_data[add_server[0]]['server'] = obj

    return module_data
