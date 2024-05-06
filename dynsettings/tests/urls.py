# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from django.conf.urls import url  # Deprecated from Django>=4.0
except ImportError:
    from django.urls import re_path as url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
