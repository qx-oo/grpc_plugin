# Django Grpc Plugin

require: python3.5+

### Install:

    $ pip install git+http://git.jian24.com/commerce/grpc_plugin.git

### Run:

run grpc server:

    $ python manage.py runserver_grpc

### Other

django settings.py:

    INSTALLED_APPS = [
        'test',
        'grpc_plugin',
        'test_proto',
        ...
    ]

create 'test_proto' app:

    project:
        - test_proto:
            - __init__.py
            - proto:
                - __init__.py
                - test.proto

create grpc_view.py in app path:

    class MyTestServicerImp(MyTestServicer):

        def hello(self, request, content):
            return test_pb2.UserInfo(info="%s, %s" % (request.id, request.name))

client:

    from grpc_plugin.client import client_channel
    from test_proto.proto import test_pb2, test_pb2_grpc
    from grpc_plugin.utils import message_to_json

    channel = client_channel("localhost:50051")
    client = test_pb2_grpc.MyTestStub(channel)
    response = client.hello(test_pb2.User(id=10, name='test'))
    print(response.info)
    print('json: ', message_to_json(response))

python type mapping:

proto	| python | description
---|---|---
double | float |
float | float |
bool | bool |
int32 | int | 变长编码. 编码负数效率低下, 打算使用负数的话可以使用 sint32
int64 | int | 变长编码. 编码负数效率低下, 打算使用负数的话可以使用 sint64
unit32 | int | 变长编码.
unit64 | int | 变长编码.
sint32 | int | 变长编码，数值有符号，负数编码效率低于int32
sint64 | int | 变长编码，数值有符号，负数编码效率低于int64
fixed32 | int | 固定4byte， 如果数值经常大于2的28次方的话效率高于uint32
fixed64 | int | 固定4byte， 如果数值经常大于2的56次方的话效率高于uint64
sfixed32 | int | 固定4byte
sfixed64 | int | 固定8byte
string | string | 字符串内容应该是 UTF-8 编码或者7-bit ASCII 文本.
bytes | byte | 任意二进制数据

enum:

    message TestRequest {
        enum Course {
            option allow_alias = true;
            PYTHON = 1;
            IOS = 2;
            ANDROID = 3;
            POS = 3;
        }
    }
