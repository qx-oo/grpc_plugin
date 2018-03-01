class BaseGrpc():
    pass


def grpc_class():
    def wrapper(wrapped):
        class WrappedClass(wrapped, BaseGrpc):
            pass

        return WrappedClass
    return wrapper
