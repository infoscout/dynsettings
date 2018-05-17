# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from dynsettings.models import Setting, SettingCache


class Value(object):
    data_type = None

    def __init__(self, key, default_value, help_text=None):
        self.key = key
        self.default_value = default_value
        self.help_text = help_text

        SettingCache.valuedict[key] = self

    def get_value(self, bucket=None):
        return SettingCache.get_value(self.key, bucket)

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
        value = self.get_value(bucket)
        if value:
            return self.convert(value)
        return value

    def set(self, force=False):
        """ Stores value in database """

        try:
            create = False
            setting = Setting.objects.get(key=self.key)

        except Setting.DoesNotExist:
            create = True
            setting = Setting()

        # save initial to db
        if create or force:
            setting.key = self.key
            setting.value = self.default_value
            setting.help_text = self.help_text
            setting.data_type = self.data_type
            setting.save()

            return True

        return False


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
        return Decimal(value)


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
