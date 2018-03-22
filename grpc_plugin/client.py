from .key import get_key
import grpc
from . import interceptor
import socket


def client_channel(addrport, ssl=False):
    """
    Get client grpc channel
    """
    def _add_header(channel, key, value):
        header_adder_interceptor = interceptor\
            .header_adder_interceptor(key, value)
        return grpc.intercept_channel(channel, header_adder_interceptor)

    if ssl:
        trusted_certs = get_key.server_crt()
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        channel = grpc.secure_channel(addrport, credentials)
    else:
        channel = grpc.insecure_channel(addrport)

    channel = _add_header(channel, 'host', socket.gethostname())
    return channel
