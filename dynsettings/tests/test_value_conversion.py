from django.test import TestCase

from decimal import Decimal
import mock

from dynsettings.values import (
    BooleanValue, DecimalValue, FloatValue, IntegerValue, ListValue,
    StringValue
)


class ValueConversionTestCase(TestCase):
    """
    Test the conversion method on child classes
    """

    def test_string_value(self):
        """
        Verify value is converted to string
        """
        value = StringValue(key="key", default_value=7)
        converted_value = value.convert(7)
        self.assertEqual(converted_value, "7")

    def test_float_value(self):
        """
        Verify value is converted to float
        """
        value = FloatValue(key="key", default_value=7)
        converted_value = value.convert(7)
        self.assertEqual(converted_value, float(7))

    def test_integer_value(self):
        """
        Verify value is converted to integer
        """
        value = IntegerValue(key="key", default_value=7)
        converted_value = value.convert('7')
        self.assertEqual(converted_value, int(7))

    def test_decimal_value(self):
        """
        Verify value is converted to decimal
        """
        value = DecimalValue(key="key", default_value=7)
        converted_value = value.convert(7)
        self.assertEqual(converted_value, Decimal(7))

    def test_list_value(self):
        """
        Verify value is converted to list
        """
        value = ListValue(key="key", default_value=7)
        converted_value = value.convert('Test')
        self.assertEqual(converted_value, ['Test'])

    def test_bool_value(self):
        """
        Verify value is converted to Boolean
        """
        value = BooleanValue(key="key", default_value=7)
        converted_value = value.convert(1)
        self.assertEqual(converted_value, True)

        value = BooleanValue(key="key", default_value=7)
        converted_value = value.convert(0)
        self.assertEqual(converted_value, False)
