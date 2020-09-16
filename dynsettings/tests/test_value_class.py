# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache
from django.test import TestCase

from dynsettings.models import SettingCache
from dynsettings.values import Value


class ValueTestCase(TestCase):
    """
    Verify parent class Value operates correctly
    """

    def setUp(self):
        # create instance of Value class
        self.value_instance = SettingCache.get_value_object('TEST_TWO')

    def tearDown(self):
        SettingCache.reset('TEST_TWO')

    def test__call__(self):
        """
        Verify __call__ returns the value from dyn_settings file and then
        set() returns false
        """
        value = self.value_instance()
        self.assertEqual(value, 100)

    def test__call__with_empty_value(self):
        """
        Check that value returns when default value is ''
        """
        self.settingcache_instance = SettingCache()
        self.no_value_instance = Value(key='EMPTY', default_value='')
        cache.set(SettingCache._get_cache_key('EMPTY'), {'default': ''})
        no_value = self.no_value_instance()
        self.assertEqual(no_value, '')

    def test_convert(self):
        """
        Verify convert returns same value from Value.convert
        """
        # no override method on Value._convert from child classes
        self.assertEqual(self.value_instance._convert('5'), 5)
