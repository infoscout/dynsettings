# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import include, re_path
from django.contrib import admin


urlpatterns = [
    re_path(r'^admin/', include('admin.site.urls'),
]
