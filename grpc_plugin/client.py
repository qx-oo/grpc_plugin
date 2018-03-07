from .key import get_key
import grpc


def client_channel(addrport):
    trusted_certs = get_key.server_crt()
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel(addrport, credentials)
    return channel
