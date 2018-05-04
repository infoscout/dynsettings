from django.test import RequestFactory, TestCase
from django.contrib import admin

import mock

from dynsettings.admin.model_admins import BucketAdmin
from dynsettings.admin.views import edit_settings
from dynsettings.models import Bucket, Setting


# We have to register the model admin so that the changelist can be tested
admin.site.register(Bucket, BucketAdmin)


class AdminViewsTestCase(TestCase):
    """
    Test the admin views are responding to get and post requests
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.bucket = Bucket.objects.create(key='BUCKET', bucket_type='Fancy')
        self.setting = Setting.objects.create(key='SET', data_type='INTEGER')

    def test_get_request(self):

        request = self.factory.get('admin/dynsettings/setting/edit')
        response = edit_settings(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('admin/dynsettings/setting/edit?search=item')
        response = edit_settings(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('admin/dynsettings/setting/edit?bucket=BUCKET')
        response = edit_settings(request)
        self.assertEqual(response.status_code, 200)

    @mock.patch('dynsettings.admin.views.messages')
    def test_post_request(self, mock_messages):

        # setting = {'key': 'OTHER', 'value': 'BAR'}
        request = self.factory.post(
                        'admin/dynsettings/setting/edit?bucket=BUCKET',
                        {self.setting: 'key'}
                    )
        response = edit_settings(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post(
                        'admin/dynsettings/setting/edit',
                        {self.setting: 'key'}
                    )
        response = edit_settings(request)
        self.assertEqual(response.status_code, 200)
