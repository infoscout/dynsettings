import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from dynsettings.models import SettingCache
from optparse import make_option

class Command(BaseCommand):
    """
    Syncsettings cmd is deprecated
    
    New dynsettings are auto saved to db upon first access. 
    """
    
    args = '<reset=False>'
    help = 'Inserts db records for dynsettings'
    
    option_list = BaseCommand.option_list + (
        make_option('--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Resets all values to default'),
        )

    def handle(self, *args, **options):
        reset = options['reset']
        
        for installed_app in settings.INSTALLED_APPS:
           
            # Try and import
            import_name = "%s.dynsettings" % installed_app
            try:
                x = __import__(import_name)
            except ImportError as exc:
                sys.stderr.write("Error: failed to import settings module {} , ({}) \n".format(import_name,exc))
                continue
            
            print "PROCESSING APP: %s" % installed_app

        # Now that they are all imported, loop through and save
        for key, value in SettingCache.valuedict.items():
            if value.set(reset): 
                print "SET: %s" % key
