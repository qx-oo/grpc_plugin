from django.shortcuts import render
from django.http import HttpResponse
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


def hello1(request):
    channel = client_channel("localhost:50051")
    client = proto1_test_pb2_grpc.YourTestStub(channel)
    response = client.hello(proto1_test_pb2.User(id=10, name='test'))
    return HttpResponse(response.info)
