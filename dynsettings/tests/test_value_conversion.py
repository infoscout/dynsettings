# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.test import TestCase

from dynsettings.values import (
    BooleanValue, DecimalValue, FloatValue, IntegerValue, ListValue,
    StringValue,
)


class ValueConversionTestCase(TestCase):
    """
    Test the conversion method for values on child classes of Value
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
        value = DecimalValue(key="key", default_value=0.002)

        converted_value = value.convert(value.default_value) * Decimal(10.00)
        self.assertEqual(converted_value, Decimal('0.02'))

        converted_value = value.convert('7.0')
        self.assertEqual(converted_value, Decimal('7.0'))

    def test_list_value(self):
        """
        Verify value is converted to list
        """
        value = ListValue(key="key", default_value=7)
        multiple_values = value.convert('Test, multiple, values')
        self.assertEqual(multiple_values, ['Test', 'multiple', 'values'])

        single_value = value.convert('single_value')
        self.assertEqual(single_value, ['single_value'])

    def test_bool_value(self):
        """
        Verify value is converted to Boolean
        """
        # check one returns True
        value = BooleanValue(key="key", default_value=7)
        converted_value = value.convert(1)
        self.assertTrue(converted_value)

        # check zero returns False
        value = BooleanValue(key="key", default_value=7)
        converted_value = value.convert(0)
        self.assertFalse(converted_value)
