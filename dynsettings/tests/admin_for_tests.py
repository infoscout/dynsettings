from django.contrib import admin

from dynsettings.admin.model_admins import SettingAdmin
from dynsettings.models import Setting


class TestingAdmin(SettingAdmin):
    """
    Test instance of SettingAdmin to check get_urls functions properly
    """
    pass


admin.site.register(Setting, TestingAdmin)
