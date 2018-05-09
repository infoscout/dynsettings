from django.contrib import admin
from django.test import Client, RequestFactory, TestCase

import mock

from dynsettings.admin.model_admins import SettingAdmin
from dynsettings.models import Setting

admin.site.register(Setting, SettingAdmin)


class SettingAdminTestCase(TestCase):
    """
    Verify SettingAdmin returns keys and false for permissions
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.setting = Setting.objects.create(key='Setting')
        self.setting_admin_test = SettingAdmin(self.setting, admin.site)
        self.client_test = Client()

    def test_key(self):
        # returns Setting instance key
        setting_key = self.setting_admin_test.key(self.setting)
        self.assertEqual(setting_key, 'Setting')

    def test_has_add_permission(self):
        # returns false for permissions
        has_permission = self.setting_admin_test.has_add_permission(self.factory)
        self.assertFalse(has_permission)

    def test_get_urls(self):
        # check edit is added to list of urls
        response = self.setting_admin_test.get_urls()
        self.assertEqual(response[0].name, 'dynsettings_setting_edit')
