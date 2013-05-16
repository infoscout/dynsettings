# DynSettings

Django app for storing key/value settings. Instead of storing settings in code (django default), settings are stored in db allowing them to be updated dynamically without code releases. 

New dynsettings are auto-saved to db upon first access, you no longer need to run `manage.py syncsettings` 

### Defining a setting

To define a new setting, add a module: `appname.dynsettings`. Example below:

	# dynsettings.py
	from infoscout.apps.dynsettings.values import IntegerValue, BooleanValue
	
	USER_REG_POINTS = IntegerValue('USER_REG_POINTS', 100, help_text="Points for a new user")
	INVITES_ENABLED = BooleanValue('INVITES_ENABLED', 1)


### Reading a setting

	from appname import dynsettings 
	
	user_points = dynsettings.USER_REG_POINTS()