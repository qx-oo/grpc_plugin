# Django Grpc Plugin

### Install:

    $ pip install git+https://github.com/qx-oo/grpc_plugin

### Run:

run grpc server:

    $ python manage.py runserver_grpc

### Other

django settings.py:

    INSTALLED_APPS = [
        'test',
        'grpc_plugin',
        ...
    ]

create grpc_view.py in app path:

    class MyTestServicerImp(MyTestServicer):

        def hello(self, request, content):
            return test_pb2.UserInfo(info="%s, %s" % (request.id, request.name))

python type mapping:

proto	| python |	描述
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
fixed32 | int | 固定4byte， 如果数值经常大于2的28次方的话效率高于uint32
fixed64 | int | 固定4byte， 如果数值经常大于2的56次方的话效率高于uint64
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
