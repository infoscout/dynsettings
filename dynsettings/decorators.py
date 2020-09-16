# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import functools

from mock import patch


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
        self.patches = []

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped_f(*args):

            # Set test values
            for dynsetting, test_value in self.list_settings:
                dyn_patch = patch(dynsetting, return_value=test_value)
                dyn_patch.start()
                self.patches.append(dyn_patch)

            try:
                # Run function
                f(*args)
            finally:
                # Clear test values
                for dyn_patch in self.patches:
                    dyn_patch.stop()

        return wrapped_f
