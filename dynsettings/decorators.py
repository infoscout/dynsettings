# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import functools


class override_dynsettings(object):
    """
    A decorator intended to be used for test cases when it is
    helpful to temporarily override a dynsettings. Example:


    from dynsettings.decorators import override_dynsettings
    from app import dyn_settings

    class AppTestCase(unittest.TestCase):

        @override_dynsettings((dyn_settings.FOO, 1), (dyn_settings.BAR, 2))
        def test_foovalue(self):
            pass
    """

    def __init__(self, *args):
        # self.dynsetting = dynsetting
        # self.test_value = test_value

        self.list_settings = args

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped_f(*args):

            # Set test values
            for dynsetting, test_value in self.list_settings:
                dynsetting.set_test_value(test_value)

            # Set test value
            # self.dynsetting.set_test_value(self.test_value)

            # Run function
            f(*args)

            # Clear test values
            for dynsetting, test_value in self.list_settings:
                dynsetting.clear_test_value()
            # self.dynsetting.clear_test_value()

        return wrapped_f
