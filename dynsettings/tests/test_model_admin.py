from django.test import RequestFactory, TestCase

import mock

from dynsettings.admin.model_admins import SettingAdmin
from dynsettings.models import Setting
from dynsettings.tests.admin_for_tests import TestingAdmin


class SettingAdminTestCase(TestCase):
    """
    Verify SettingAdmin returns keys and false for permissions
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.factory.name = None
        self.setting = Setting.objects.create(key='Setting')
        self.setting_admin_test = SettingAdmin(self.setting, self.factory)


    def test_key(self):
        # returns Setting instance key
        setting_key = self.setting_admin_test.key(self.setting)
        self.assertEqual(setting_key, 'Setting')

    def test_has_add_permission(self):
        # returns false for permissions
        has_permission = self.setting_admin_test.has_add_permission(self.factory)
        self.assertFalse(has_permission)

    def test_get_urls(self):
        # create instance of TestingAdmin to check instantiation of get_urls
        self.testing_admin_instance = TestingAdmin(self.setting, self.factory)
