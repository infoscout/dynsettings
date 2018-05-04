from django.test import RequestFactory, TestCase

import mock

from dynsettings.admin.model_admins import SettingAdmin
from dynsettings.models import Setting


class SettingAdminTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.factory.name = None
        self.setting = Setting.objects.create(key='Setting')
        self.setting_admin_test = SettingAdmin(self.setting, self.factory)

    def test_key(self):
        setting_key = self.setting_admin_test.key(self.setting)
        self.assertEqual(setting_key, 'Setting')

    def test_has_add_permission(self):
        has_permission = self.setting_admin_test.has_add_permission(self.factory)
        self.assertFalse(has_permission)

    # @mock.patch('dynsettings.admin.model_admins.SettingAdmin.get_urls')
    # def test_urls(self, mock_admin_view):
    #     mock_admin_view.return_value = 'returned_urls'
    #     urls = self.setting_admin_test.get_urls()
    #     self.assertEqual(urls, 'stuff')
