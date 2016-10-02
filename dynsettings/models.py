from collections import defaultdict

from django.conf import settings
from django.core.cache import cache
from django.db import models, transaction
from django.db.utils import DatabaseError, IntegrityError


DATA_TYPES = (
    ('STRING', 'String'),
    ('INTEGER', 'Integer'),
    ('FLOAT', 'Float'),
    ('DECIMAL', 'Decimal'),
    ('BOOLEAN', 'Boolean'),
    ('LIST', 'List'),
)


class Setting(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = models.TextField(blank=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES, blank=False)

    def __nonzero__(self):
        return self.key is not None

    def save(self, *args, **kwargs):
        # Save and reload cache
        super(Setting, self).save(*args, **kwargs)
        cache_key = "{} {}".format(self.key, None)
        value = cache.set(cache_key, self.value)

    def __unicode__(self):
        return self.key


class Bucket(models.Model):
    key = models.CharField(max_length=16, primary_key=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    bucket_type = models.CharField(max_length=32, blank=True)
    probability = models.IntegerField(default=0, help_text="Used for other apps that may choose random buckets")

    def __unicode__(self):
        return self.key


class BucketSetting(models.Model):
    bucket = models.ForeignKey(Bucket)
    setting = models.ForeignKey(Setting)
    value = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (('bucket', 'setting'))

    def save(self, *args, **kwargs):
        # Save and reload cache
        super(BucketSetting, self).save(*args, **kwargs)
        SettingCache.load()


class SettingCache():
    """
    Static class used to load and provide values
    """

    _override_values = {}
    _values = defaultdict(dict)
    _exists_on_database = set()
    _loaded = False
    _v = {}

    @classmethod
    def get_value(cls, key, bucket=None):
        # Preference 1) Retrieve from the override values.
        if key in cls._override_values:
            return cls._override_values[key]

        # Preference 2) Retrieve from cache. Check if there's a value with the
        # bucket, if provided, before trying the default.
        # for b in [bucket, None] if bucket else [None]:
        #     cache_key = "{} {}".format(key, b)
        #     value = cache.get(cache_key)
        #     if value is not None:
        #         return value
        cache_key = "{} {}".format(key, bucket)
        value = cache.get(cache_key)
        if value is not None:
            return value

        # Preference 3) Retrieve from database and update cache.
        value = cls.get_value_from_database(key)
        if value is not None:
            cache.set(cache_key, value)
            return value

        # Preference 4) Retrieve from code and update database and cache.
        value_object = cls._v[key]
        cls.update_database(value_object) # Updates cache in Setting.save()
        return value_object.default_value

    @classmethod
    def get_value_from_database(cls, key):
        try:
            return Setting.objects.get(key=key).value
        except (DatabaseError, Setting.DoesNotExist):
            return None

    @classmethod
    def update_database(cls, value_object):
        try:
            Setting.objects.create(
                key=value_object.key,
                value=value_object.default_value,
                help_text=value_object.help_text)
        except (DatabaseError, IntegrityError):
            pass

    @classmethod
    def clear_cache(cls):
        for value_object in cls._v.itervalues():
            cache_key = "{} {}".format(value_object.key, None)
            cache.delete(cache_key)
