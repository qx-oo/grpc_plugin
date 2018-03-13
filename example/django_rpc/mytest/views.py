from django.http import HttpResponse
import json
from grpc_plugin.client import client_channel
from test_proto.proto import (
    test_pb2,
    test_pb2_grpc,
)
from test_proto1.proto import test_pb2 as proto1_test_pb2
from test_proto1.proto import test_pb2_grpc as proto1_test_pb2_grpc

# Create your views here.


def hello(request):
    channel = client_channel("localhost:50051")
    client = test_pb2_grpc.MyTestStub(channel)
    response = client.hello(test_pb2.User(id=10, name='test'))
    return HttpResponse(response.info)


def _user_list(user_list):
    for user in user_list:
        yield user


def hello_request_stream(request):
    channel = client_channel("localhost:50051")
    client = proto1_test_pb2_grpc.YourTestStub(channel)

    user_list = [
        proto1_test_pb2.User(id=i, name='test%s' % i)
        for i in range(10)
    ]
    response = client.hello(_user_list(user_list))
    return HttpResponse(response.info)


def hello_response_stream(request):
    channel = client_channel("localhost:50051")
    client = proto1_test_pb2_grpc.YourTest1Stub(channel)
    response = client.hello(proto1_test_pb2.User(id=1, name='test'))

    info = [
        user_info.info
        for user_info in response
    ]
    return HttpResponse(json.dumps(info))


def hello_request_response_stream(request):
    channel = client_channel("localhost:50051")
    client = proto1_test_pb2_grpc.YourTest2Stub(channel)
    user_list = [
        proto1_test_pb2.User(id=i, name='test%s' % i)
        for i in range(10)
    ]
    response = client.hello(_user_list(user_list))

    info = [
        user_info.info
        for user_info in response
    ]
    return HttpResponse(json.dumps(info))


def hello_list(request):
    channel = client_channel("localhost:50051")
    client = proto1_test_pb2_grpc.YourTest3Stub(channel)
    user_list = [
        proto1_test_pb2.User(id=i, name='test%s' % i)
        for i in range(10)
    ]
    response = client.hello(proto1_test_pb2.AllUser(user_list=user_list,
                                                    desc='123'))
    info = [
        user_info.info
        for user_info in response.userinfo_list
    ]
    return HttpResponse(json.dumps(info))
