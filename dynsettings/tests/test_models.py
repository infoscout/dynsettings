from django.db.utils import DatabaseError
from django.test import TestCase

import mock

from dynsettings.models import Bucket, BucketSetting, Setting, SettingCache


class SettingTestCase(TestCase):
    """
    Verify Setting class performs as expected
    """

    def setUp(self):
        # ask if this is the conventional way to do it or if object.create is
        self.setting_instance = Setting(key='TEST', data_type=('STRING', 'String'))

    def test__unicode__(self):
        self.assertEqual(self.setting_instance.__unicode__(), 'TEST')

    def test__nonzero__(self):
        self.assertEqual(self.setting_instance.__nonzero__(), True)


class BucketTestCase(TestCase):
    """
    Verify Bucket class performs as expected
    """

    def setUp(self):
        self.bucket_instance = Bucket(key='TEST')

    def test__unicode__(self):
        self.assertEqual(self.bucket_instance.__unicode__(), 'TEST')


class SettingCacheTestCase(TestCase):
    """
    Verify SettingCache is normal
    """

    def setUp(self):
        self.cache_instance = SettingCache()
        self.cache_instance._test_values['TEST'] = 'testing'
        self.setting_instance = Setting(
                                        key='TESTING',
                                        data_type=('STRING', 'String')
                                )

    def tearDown(self):
        SettingCache.reset()

    def test_get_value(self):
        self.bucket_instance = Bucket(key='TEST')
        self.assertEqual(self.cache_instance.get_value('TEST'), 'testing')


class DBError(TestCase):
    def setUp(self):
        self.cache_instance = SettingCache()
        self.setting = Setting.objects.create(key='TEST_TWO', data_type=('STRING', 'String'))
        self.bucket = Bucket.objects.create(key='BUCKET')
        self.bucket_setting = BucketSetting.objects.get_or_create(bucket=self.bucket, setting=self.setting, value='VALUE')

    def tearDown(self):
        SettingCache.reset()

    @mock.patch('dynsettings.models.Setting.objects.all')
    def test_load(self, mock_settings_queryset_all):
        # testing load doesn't work when database error
        mock_settings_queryset_all.side_effect = DatabaseError

        loaded = self.cache_instance.load()
        self.assertEqual(loaded, False)

    @mock.patch('dynsettings.models.SettingCache.load')
    def test_get_value_with_result_false(self, mock_settings_load):
        mock_settings_load.return_value = False

        value = self.cache_instance.get_value('TEST_TWO')
        self.assertEqual(value, 100)

    def test_cls_value_keys(self):
        value = self.cache_instance.get_value('TEST_TWO', self.bucket)

        self.assertEqual(value, 'VALUE')
