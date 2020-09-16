# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.utils import DatabaseError
from django.test import TestCase
import mock
import six

from dynsettings.models import Bucket, BucketSetting, Setting, SettingCache


class SettingModelTestCase(TestCase):
    """
    Verify Setting class methods operate correctly
    """

    def setUp(self):
        self.setting_instance = Setting(key='TEST', data_type='STRING')

    def test__unicode__(self):
        setting_str = six.text_type(self.setting_instance)
        self.assertEqual('TEST', setting_str)

    def test__nonzero__(self):
        self.assertEqual(bool(self.setting_instance), True)


class BucketModelTestCase(TestCase):
    """
    Verify Bucket class returns correct unicode representation
    """

    def setUp(self):
        self.bucket_instance = Bucket(key='TEST')

    def test__unicode__(self):
        bucket_str = six.text_type(self.bucket_instance)
        self.assertEqual(bucket_str, 'TEST')


class SettingCacheValueTestCase(TestCase):
    """
    Verify SettingCache stores values as expected
    """

    def setUp(self):
        self.cache_instance = SettingCache()
        self.cache_instance._test_values['TEST'] = 'testing'

    def tearDown(self):
        # reset cache for each test so loaded resets
        del self.cache_instance._test_values['TEST']

    def test_get(self):
        # check cache instance returns correct key
        self.assertEqual(self.cache_instance.get('TEST'), 'testing')


class SettingCacheTestCase(TestCase):
    """
    Verify additional logic runs in SettingCache, including errors
    """

    def setUp(self):
        self.cache_instance = SettingCache()
        self.setting = Setting.objects.create(
            key='ANOTHER_TEST',
            data_type='STRING'
        )
        self.bucket = Bucket.objects.create(key='BUCKET')
        self.bucket_setting = BucketSetting.objects.get_or_create(
            bucket=self.bucket,
            setting=self.setting,
            value='VALUE'
        )

    def test_get_with_result_false(self):
        value = self.cache_instance.get('TEST_THREE')
        self.assertEqual(value, 200)

    def test_cls_value_keys(self):
        """
        Test bucket.key value returned when bucket and bucket.key in
        cls._values[key]
        """
        value = self.cache_instance.get('ANOTHER_TEST', self.bucket)

        self.assertEqual(value, 'VALUE')

    @mock.patch('dynsettings.models.SettingCache.import_dynsetting_from_app')
    def test_import_dynsetting(self, mock_error):
        """
        Check import_dynsetting throws error if ImportError other than no
        module named dyn_settings occurs
        """
        mock_error.side_effect = ImportError('Unique error')

        with self.assertRaises(ImportError):
            self.cache_instance.import_value_object(key='Nothing')
