from django.conf.urls.defaults import patterns, url
from isc_admin.admin_site import AdminApp
from dynsettings.admin.model_admins import SettingAdmin, \
    BucketAdmin
from dynsettings.admin.views import edit_settings
from dynsettings.models import Setting, Bucket


class DynsettingsAdminApp(AdminApp):
    def get_urls(self):
        urls = patterns('',
            url(r'^dynsettings/?$', self.admin_view(edit_settings), name='dynsettings'),
        )
        return urls
    
DynsettingsAdminApp.register(Setting, SettingAdmin)
DynsettingsAdminApp.register(Bucket, BucketAdmin)