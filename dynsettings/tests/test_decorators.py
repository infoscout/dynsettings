from django.test import TestCase

import dyn_settings

from dynsettings.decorators import override_dynsettings
from dynsettings.models import SettingCache
from dynsettings.values import Value


class OverrideTestCase(TestCase):
    """
    Verify the override dynsettings decorator changes values for tests
    """

    def setUp(self):
        self.value_instance = Value(key='TEST_THREE', default_value=None)

    def test_decorator(self):
        # first value set for TEST_THREE is 'Start Value'
        self.value_instance.set_test_value('Start Value')
        self.assertEqual(SettingCache._test_values['TEST_THREE'], 'Start Value')

    @override_dynsettings((dyn_settings.TEST_THREE, 'override'))
    def test_decorator_changed_value(self):
        # value changes to 'override'
        self.assertEqual(SettingCache._test_values['TEST_THREE'], 'override')
