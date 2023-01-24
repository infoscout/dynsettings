# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta

from decimal import Decimal

from dynsettings.models import SettingCache


class Value(object):
    data_type = None

    def __init__(self, key, default_value, help_text=None, cache_local_time=300):
        self.key = key
        self.default_value = default_value
        self.help_text = help_text

        self.cache_local_time = cache_local_time
        self.local_cache_expires_at = None
        self.local_cache = None

        SettingCache.setup_value_object(self)

    def get(self, bucket=None):
        if self.local_cache is not None and datetime.now() < self.local_cache_expires_at:
            return self.local_cache

        value = SettingCache.get(self.key, bucket)
        if self.cache_local_time:
            self.local_cache = value
            self.local_cache_expires_at = datetime.now() + timedelta(secs=self.cache_local_time)
        return value

    def set_test_value(self, value):
        """
        Sets a test value. Useful when needed to override dynsettings
        for test cases and set a test value
        """
        SettingCache._test_values[self.key] = value

    def clear_test_value(self):
        if self.key in SettingCache._test_values:
            del SettingCache._test_values[self.key]

    def convert(self, value):
        """
        Override in child classes
        """
        return value

    def __call__(self, bucket=None):
        value = self.get(bucket)
        if value:
            return self.convert(value)
        return value


class StringValue(Value):
    data_type = 'STRING'

    def convert(self, value):
        return str(value)


class FloatValue(Value):
    data_type = 'FLOAT'

    def convert(self, value):
        return float(value)


class IntegerValue(Value):
    data_type = 'INTEGER'

    def convert(self, value):
        return int(value)


class DecimalValue(Value):
    data_type = 'DECIMAL'

    def convert(self, value):
        # Coerce to string to help reduce floating point errors
        return Decimal(str(value))


class ListValue(Value):
    data_type = 'LIST'

    def convert(self, value):
        return list(map(lambda s: s.strip(), value.split(",")))


class BooleanValue(Value):
    data_type = 'BOOLEAN'

    def convert(self, value):
        val = int(value)
        if val == 1:
            return True
        else:
            return False
