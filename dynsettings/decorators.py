# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import functools

import mock


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
        self.list_settings = args

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped_f(*args):

            # Set test values
            for dynsetting, test_value in self.list_settings:
                dynsetting = mock.Mock(spec=dynsetting.__class__, return_value=test_value)

            # Run function
            f(*args)

        return wrapped_f
