# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from dynsettings.models import SettingCache


class Value(object):
    data_type = None

    def __init__(self, key, default_value, help_text=None):
        self.key = key
        self.default_value = default_value
        self.help_text = help_text

        SettingCache.setup_value_object(self)

    def get(self, bucket=None):
        return SettingCache.get(self.key, bucket)

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
