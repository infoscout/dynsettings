# DynSettings

Django app for storing key/value settings. Instead of storing settings in code (django default), settings are stored in db allowing them to be updated dynamically without code releases. 

### Defining a setting

To define a new setting, add a module: `appname.dyn_settings`. Example below:

	# dynsettings.py
	from dynsettings.values import IntegerValue, BooleanValue
	
	USER_REG_POINTS = IntegerValue('USER_REG_POINTS', 100, help_text="Points for a new user")
	INVITES_ENABLED = BooleanValue('INVITES_ENABLED', 1)


### Reading a setting

	from appname import dyn_settings 
	
	user_points = dyn_settings.USER_REG_POINTS()