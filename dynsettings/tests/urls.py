# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^admin/', include('admin.site.urls')),
]
