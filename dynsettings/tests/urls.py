# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

app_name = 'dynsettings'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
