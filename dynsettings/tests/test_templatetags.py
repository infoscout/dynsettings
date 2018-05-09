from django.test import TestCase

from dynsettings.models import SettingCache
from dynsettings.templatetags.dynsettings import get_dynsetting
from dynsettings.values import Value


class TemplateTagsTestCase(TestCase):
    """
    Verify get_dynsetting returns valuedict
    """
    def setUp(self):
        self.cache_instance = SettingCache()
        self.value_instance = Value(key='key', default_value='default_value')

    def tearDown(self):
        self.value_instance.clear_test_value()

    def test_get_dynsetting(self):
        setting_value_dict = get_dynsetting('TEST_ONE')
        self.assertEqual(setting_value_dict, 150)
