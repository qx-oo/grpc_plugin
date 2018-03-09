from test_proto.proto.test_pb2_grpc import MyTestServicer
from test_proto.proto import test_pb2
from test_proto1.proto.test_pb2_grpc import YourTestServicer
from test_proto1.proto import test_pb2 as proto1_test_pb2
import logging


log = logging.getLogger()


class MyTestServicerImp(MyTestServicer):

    def hello(self, request, content):
        log.info('request')
        return test_pb2.UserInfo(info="%s, %s" % (request.id, request.name))


class YourTestServicerImp(YourTestServicer):

    def hello(self, request, context):
        log.info('request')
        return proto1_test_pb2.UserInfo(info="1: %s, %s" % (request.id,
                                                            request.name))
