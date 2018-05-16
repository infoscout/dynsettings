# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from dynsettings.admin.views import edit_settings


class DynsettingsAdminApp(admin.ModelAdmin):

    def get_urls(self):
        return [
            url(
                r'^dynsettings/?$',
                self.admin_site.admin_view(edit_settings),
                name='dynsettings'
            ),
        ]
