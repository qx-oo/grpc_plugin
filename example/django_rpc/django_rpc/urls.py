"""django_rpc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from mytest.views import (
    hello,
    hello_request_stream,
    hello_response_stream,
    hello_request_response_stream,
    )

urlpatterns = [
    url(r'^hello/', hello),
    url(r'^hello_request/', hello_request_stream),
    url(r'^hello_response/', hello_response_stream),
    url(r'^hello_request_response/', hello_request_response_stream),
    url(r'^admin/', admin.site.urls),
]
