# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path, include
from django.contrib import admin

api_urls = (
    [
        path('account/', include('account.urls')),
    ],
    'api'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls))
]
