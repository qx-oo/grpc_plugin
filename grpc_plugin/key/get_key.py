import os


def server_key():
    path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(path, 'server.key'), 'rb') as f:
        private_key = f.read()
    return private_key


def server_crt():
    path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(path, 'server.crt'), 'rb') as f:
        certificate_chain = f.read()
    return certificate_chain
