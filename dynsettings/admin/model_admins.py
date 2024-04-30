# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from django.conf.urls import url  # Deprecated from Django>=4.0
except ImportError:
    from django.urls import re_path as url
from django.contrib import admin

from dynsettings.admin.views import edit_settings
from dynsettings.models import BucketSetting


class BucketSettingInline(admin.TabularInline):
    model = BucketSetting


class SettingAdmin(admin.ModelAdmin):

    # Changelist files
    list_display = ('key', 'value', 'help_text', 'data_type',)
    list_editable = ('value',)
    # linked_display_links = ()

    fields = ('key', 'value', 'data_type',)
    readonly_fields = ('key', 'help_text', 'data_type',)
    search_fields = ('key',)
    ordering = ('key',)
    actions = []

    inlines = [BucketSettingInline]

    def key(self, obj):
        return obj.key

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super(SettingAdmin, self).get_urls()
        my_urls = [
            url(
                r'^edit/?$',
                self.admin_site.admin_view(edit_settings),
                name='dynsettings_setting_edit'
            ),
        ]
        return my_urls + urls


class BucketAdmin(admin.ModelAdmin):
    list_display = ('key', 'bucket_type', 'probability', 'desc',)
    list_editable = ('probability',)
    ordering = ('key',)

    pass
