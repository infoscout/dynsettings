from decimal import Decimal

from django.db import transaction
from django.db.utils import IntegrityError

from models import SettingCache, Setting


class Value(object):
    data_type = None

    def __init__(self, key, default_value, help_text=None):
        self.key = key
        self.default_value = str(default_value)
        self.help_text = help_text

        SettingCache._values[key]['object'] = self
        SettingCache._v[key] = self

    def get_value(self, bucket=None):
        return SettingCache.get_value(self.key, bucket)

    def set_override_value(self, value):
        """
        Sets a test value. Useful when needed to override dynsettings
        for test cases and set a test value
        """
        SettingCache._override_values[self.key] = value

    def clear_override_value(self):
        if self.key in SettingCache._override_values:
            del SettingCache._override_values[self.key]

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

    @transaction.commit_on_success
    def update_db_with_new_setting(self):
        """
        Avoids get_or_create race condition
        """
        try:
            Setting.objects.create(
                key=self.key,
                value=self.default_value,
                help_text=self.help_text,
                data_type=self.data_type)
        except IntegrityError:
            pass


#
#   Warning! Don't make a value that can store None. This is because values are
#   kept in memcache, and memcache returns None to indicate a missing key, so
#   SettingCache ignores None.
#


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
        return [s.strip() for s in value.split(",")]


class BooleanValue(Value):
    data_type = 'BOOLEAN'
    def convert(self, value):
        val = int(value)
        return val == 1
