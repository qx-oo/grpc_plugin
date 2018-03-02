# Django Grpc Plugin

### Install:

    $ pip install git+https://github.com/qx-oo/grpc_plugin

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

run grpc server:

    $ python manage.py runserver_grpc
