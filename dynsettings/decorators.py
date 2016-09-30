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
        self.settings_and_override_values = args

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped_f(*args):

            # Set values
            for dynsetting, override_value in self.settings_and_override_values:
                dynsetting.set_override_value(override_value) 

            # Run function
            f(*args)

            # Clear values
            for dynsetting, override_value in self.settings_and_override_values:
                dynsetting.clear_override_value()

        return wrapped_f
