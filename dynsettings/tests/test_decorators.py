# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from dynsettings.decorators import override_dynsettings
from dynsettings.models import SettingCache
from dynsettings.tests import dyn_settings


class OverrideDynsettingsTestCase(TestCase):
    """
    Verify the override dynsettings decorator changes values for tests
    """

    @override_dynsettings((dyn_settings.TEST_THREE, 'override',))
    def test_decorator_changed_value(self):
        # value changes to 'override'
        self.assertEqual(dyn_settings.TEST_THREE, 'override')
