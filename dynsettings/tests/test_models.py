from django.db.utils import DatabaseError
from django.test import TestCase

import mock
from mock import patch

from dynsettings.models import Bucket, BucketSetting, Setting, SettingCache


class SettingTestCase(TestCase):
    """
    Verify Setting class methods operate correctly
    """

    def setUp(self):
        self.setting_instance = Setting(
            key='TEST', data_type=('STRING', 'String')
        )

    def test__unicode__(self):
        self.assertEqual(self.setting_instance.__unicode__(), 'TEST')

    def test__nonzero__(self):
        self.assertEqual(self.setting_instance.__nonzero__(), True)


class BucketTestCase(TestCase):
    """
    Verify Bucket class returns correct unicode representation
    """

    def setUp(self):
        self.bucket_instance = Bucket(key='TEST')

    def test__unicode__(self):
        self.assertEqual(self.bucket_instance.__unicode__(), 'TEST')


class SettingCacheValueTestCase(TestCase):
    """
    Verify SettingCache stores values as expected
    """

    def setUp(self):
        self.cache_instance = SettingCache()
        self.cache_instance._test_values['TEST'] = 'testing'

    def tearDown(self):
        # reset cache for each test so loaded resets
        SettingCache.reset()
        del self.cache_instance._test_values['TEST']

    def test_get_value(self):
        # check cache instance returns correct key
        self.assertEqual(self.cache_instance.get_value('TEST'), 'testing')


class SettingCacheTestCase(TestCase):
    """
    Verify additional logic runs in SettingCache, inlcuding errors
    """
    def setUp(self):
        self.cache_instance = SettingCache()
        self.setting = Setting.objects.create(
            key='TEST_TWO', data_type=('STRING', 'String')
        )
        self.bucket = Bucket.objects.create(key='BUCKET')
        self.bucket_setting = BucketSetting.objects.get_or_create(
            bucket=self.bucket, setting=self.setting, value='VALUE'
        )

    def tearDown(self):
        SettingCache.reset()

    # set mock for Setting.objects.all() resulting in DatabaseError
    @mock.patch('dynsettings.models.Setting.objects.all')
    def test_load(self, mock_settings_queryset_all):
        # check database error in load function
        mock_settings_queryset_all.side_effect = DatabaseError
        loaded = self.cache_instance.load()

        self.assertEqual(loaded, False)

    # set mock for load result = False
    @mock.patch('dynsettings.models.SettingCache.load')
    def test_get_value_with_result_false(self, mock_settings_load):
        # check false result returned from cls.load call inside get_value
        mock_settings_load.return_value = False
        value = self.cache_instance.get_value('TEST_THREE')

        self.assertEqual(value, 200)

    def test_cls_value_keys(self):
        """
        Test bucket.key value returned when bucket and bucket.key in
        cls._values[key]
        """
        value = self.cache_instance.get_value('TEST_TWO', self.bucket)

        self.assertEqual(value, 'VALUE')

    def test_import_dynsetting(self):
        """
        Check import_dynsetting throws error if Importerror other than no
        module named dyn_settings occurs
        """
        with patch.object(SettingCache, 'import_dynsetting_from_app') as mock_fail:
            mock_fail.side_effect = ImportError('Unique error')

            with self.assertRaises(ImportError):
                self.cache_instance.import_dynsetting(key='Nothing')
