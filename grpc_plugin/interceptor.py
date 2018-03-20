import grpc
from . import generic_client_interceptor
import collections
import logging
from threading import local


log = logging.getLogger()


def close_old_connections():
    """检查关闭django不可用连接"""
    connections = local()
    if hasattr(connections, 'default'):
        conn = getattr(connections, 'default')
        conn.close_if_unusable_or_obsolete()


class RequestInterceptor(grpc.ServerInterceptor):

    def intercept_service(self, continuation, handler_call_details):
        close_old_connections()
        header = dict(handler_call_details.invocation_metadata)
        method = handler_call_details.method
        host = header.get('host', '')
        log.info('%s "%s"' % (host, method))
        ret = continuation(handler_call_details)
        return ret


class _ClientCallDetails(
        collections.namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    pass


def header_adder_interceptor(header, value):

    def intercept_call(client_call_details, request_iterator, request_streaming,
                       response_streaming):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append((
            header,
            value,
        ))
        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)
        return client_call_details, request_iterator, None

    return generic_client_interceptor.create(intercept_call)
