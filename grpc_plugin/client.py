from .key import get_key
import grpc


def client_channel(addrport, ssl=False):
    if ssl:
        trusted_certs = get_key.server_crt()
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        channel = grpc.secure_channel(addrport, credentials)
    else:
        channel = grpc.insecure_channel(addrport)
    return channel
