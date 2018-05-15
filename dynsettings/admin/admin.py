from django.conf.urls import url
from isc_admin.admin_site import AdminApp

from dynsettings.admin.model_admins import BucketAdmin, SettingAdmin
from dynsettings.admin.views import edit_settings
from dynsettings.models import Bucket, Setting


class DynsettingsAdminApp(AdminApp):

    def get_urls(self):
        return [
            url(r'^dynsettings/?$', self.admin_view(edit_settings),
                name='dynsettings'),
        ]


DynsettingsAdminApp.register(Setting, SettingAdmin)
DynsettingsAdminApp.register(Bucket, BucketAdmin)
