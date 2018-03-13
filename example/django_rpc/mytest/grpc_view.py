from test_proto.proto.test_pb2_grpc import MyTestServicer
from test_proto.proto import test_pb2
from test_proto1.proto.test_pb2_grpc import (
    YourTestServicer,
    YourTest1Servicer,
    YourTest2Servicer,
    YourTest3Servicer,
    )
from test_proto1.proto import test_pb2 as proto1_test_pb2
import logging


log = logging.getLogger()


class MyTestServicerImp(MyTestServicer):

    def hello(self, request, content):
        log.info('MyTestServicerImp')
        return test_pb2.UserInfo(info="%s, %s" % (request.id, request.name))


class YourTestServicerImp(YourTestServicer):

    def hello(self, request_iterator, context):
        log.info('YourTestServicerImp')
        for user in request_iterator:
            print('user: %s, %s' % (user.id, user.name))
        return proto1_test_pb2.UserInfo(info="steam request")


class YourTest1ServicerImp(YourTest1Servicer):

    def hello(self, request, context):
        log.info('YourTest1ServicerImp')
        for i in range(10):
            yield proto1_test_pb2.UserInfo(info="%s: %s, %s" % (i, request.id,
                                                                request.name))


class YourTest2ServicerImp(YourTest2Servicer):

    def hello(self, request_iterator, context):
        log.info('YourTest2ServicerImp')
        for user in request_iterator:
            yield proto1_test_pb2.UserInfo(info="%s, %s" % (user.id,
                                                            user.name))


class YourTest3ServicerImp(YourTest3Servicer):

    def hello(self, request, context):
        log.info('YourTest3ServicerImp')
        log.info('YourTest3ServicerImp: %s, %s' % (request.no_data,
                                                   request.desc))
        userinfo_list = [
            proto1_test_pb2.UserInfo(info="%s, %s" % (user.id, user.name))
            for user in request.user_list
        ]
        return proto1_test_pb2.AllUserInfo(userinfo_list=userinfo_list)
