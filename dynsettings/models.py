# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

logger = logging.getLogger('dynsettings')

DATA_TYPES = (
    ('STRING', 'String',),
    ('INTEGER', 'Integer',),
    ('FLOAT', 'Float',),
    ('DECIMAL', 'Decimal',),
    ('BOOLEAN', 'Boolean',),
    ('LIST', 'List',),
)


@python_2_unicode_compatible
class Setting(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = models.TextField(blank=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    data_type = models.CharField(
        max_length=20, choices=DATA_TYPES, blank=False
    )

    def __nonzero__(self):
        return self.key is not None

    def save(self, *args, **kwargs):
        # Save and reset cache
        super(Setting, self).save(*args, **kwargs)
        SettingCache.reset(self.key)

    def __str__(self):
        return self.key


@python_2_unicode_compatible
class Bucket(models.Model):
    key = models.CharField(max_length=16, primary_key=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    bucket_type = models.CharField(max_length=32, blank=True)
    probability = models.IntegerField(
        default=0,
        help_text="Used for other apps that may choose random buckets"
    )

    def __str__(self):
        return self.key


class BucketSetting(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (('bucket', 'setting',),)

    def save(self, force_insert=False, force_update=False, using=None):
        # Save and reset cache
        super(BucketSetting, self).save(force_insert, force_update, using)
        SettingCache.reset(self.setting.key)


class SettingCache:
    """ Static class used to load and provide values """

    value_objects = {}
    _test_values = {}

    @classmethod
    def setup_value_object(cls, value):
        """ Stores value in database """
        cls.value_objects[value.key] = value

    @classmethod
    def get_value_object(cls, key):
        if key not in cls.value_objects:
            value_object = cls.import_value_object(key)
            cls.setup_value_object(value_object)

        return cls.value_objects[key]

    @classmethod
    def get(cls, key, bucket=None):

        # First check if a testvalue set
        if key in cls._test_values:
            return cls._test_values[key]

        # Set the cache key as the key value prepended with 'dynsettings-'
        cache_key = cls._get_cache_key(key)

        # Get the value from cache
        value = cache.get(cache_key)

        if not value:
            logger.info('Cache miss: {key}'.format(key=key))
            value_object = cls.get_value_object(key)
            value = cls._load_from(value_object)

        if not value:
            raise Exception(
                (
                    "DynSetting could not be retrieved from cache or database: {cache_key}"
                ).format(cache_key=cache_key)
            )

        # First try and pull bucket
        if bucket and bucket.key in value:
            return value[bucket.key]
        else:
            return value['default']

    @classmethod
    def import_dynsetting_from_app(cls, app, key):
        """
        Returns value from key in dyn_settings module in Django app
        """
        import_name = "{}.dyn_settings".format(app.name)
        x = __import__(import_name, fromlist=[key])
        if hasattr(x, key):
            value = getattr(x, key)
            return value

    @classmethod
    def import_value_object(cls, key):
        """
        Iterates through installed apps and
        returns Dynsetting Value based on key
        """
        for app in apps.get_app_configs():
            try:
                value = cls.import_dynsetting_from_app(app, key)
                if value:
                    return value
            except ImportError as e:
                if "No module named" in str(e) and "dyn_settings" in str(e):
                    continue
                # Reimport which fires error with complete ImportError msg
                raise e

    @classmethod
    def get_or_create_from_value_object(cls, value, force=False):
        try:
            create = False
            setting = Setting.objects.get(key=value.key)
        except Setting.DoesNotExist:
            create = True
            setting = Setting()

        # save initial to db
        if create or force:
            setting.key = value.key
            setting.value = value.default_value
            setting.help_text = value.help_text
            setting.data_type = value.data_type
            setting.save()

        return setting

    @classmethod
    def _load_from(cls, value_object):
        """
        Loads dynsettings lazily
        """
        setting_record = cls.get_or_create_from_value_object(value_object)

        cache_key = cls._get_cache_key(value_object.key)
        default_value = setting_record.value
        setting_values = {'default': default_value}

        for bs in BucketSetting.objects.filter(setting=setting_record):
            bucket_key = bs.bucket.key
            setting_values[bucket_key] = bs.value

        cache.set(cache_key, setting_values)

        return setting_values

    @classmethod
    def reset(cls, key):
        logger.info('Clearing cached value for {key}'.format(key=key))
        cache_key = cls._get_cache_key(key)
        cache.delete(cache_key)

    @classmethod
    def _get_cache_key(cls, key):
        return 'dynsettings-{key}'.format(key=key)
