from django.test import TestCase

from dynsettings.models import SettingCache
from dynsettings.values import Value


class ValueTestCase(TestCase):
    """
    Verify parent class Value operates correctly
    """

    def setUp(self):
        # create instance of Value class
        self.value_instance = Value(key='TEST_TWO', default_value=None)
        # Setting.objects.create(key='dynsettings', default_value='12')

    def tearDown(self):
        SettingCache.reset()

    def test__call__(self):
        """
        Verfiy __call__ returns the value from dyn_settings file and then
        set() returns false
        """
        value = self.value_instance.__call__()
        self.assertEqual(value, '100')

        # test .set() returns false when value is already in database
        reset = self.value_instance.set()
        self.assertEqual(reset, False)

    def test_set_and_clear_test_value(self):
        """
        Verify set test value is updating SettingCache
        """
        self.value_instance.set_test_value('Changed')
        self.assertEqual(SettingCache._test_values['TEST_TWO'], 'Changed')

        self.value_instance.clear_test_value()
        self.assertEqual(SettingCache._test_values, {})

    def test_get_value(self):
        pass

    def test_convert(self):
        """
        Verify convert returns same value from Value.convert
        """
        self.assertEqual(self.value_instance.convert('5'), '5')
