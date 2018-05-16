# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.test import RequestFactory, TestCase
import mock

from dynsettings.admin.model_admins import BucketAdmin
from dynsettings.admin.views import edit_settings
from dynsettings.models import Bucket, Setting


# We have to register the model admin so that the changelist can be tested
admin.site.register(Bucket, BucketAdmin)


class AdminViewsTestCase(TestCase):
    """
    Test the admin views are responding correctly to get and post requests
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.bucket = Bucket.objects.create(key='BUCKET', bucket_type='type')
        self.setting = Setting.objects.create(
            key='SET',
            value='Firstval',
            data_type='INTEGER'
        )

        # get request with search parameter
        request = self.factory.get(
            'admin/dynsettings/setting/edit?search=item'
        )
        response = edit_settings(request)
        self.assertIn(b'item', response.content)
        self.assertEqual(response.status_code, 200)

        # get request with bucket parameter
        request = self.factory.get(
            'admin/dynsettings/setting/edit?bucket=BUCKET'
        )
        response = edit_settings(request)
        self.assertIn(b'BUCKET', response.content)
        self.assertIn(b'Firstval', response.content)
        self.assertEqual(response.status_code, 200)

    @mock.patch('dynsettings.admin.views.messages')
    def test_post_request(self, mock_messages):
        # post request with bucket and setting key
        request = self.factory.post(
            'admin/dynsettings/setting/edit?bucket=BUCKET',
            {self.setting: 'NEW'}
        )
        response = edit_settings(request)
        self.assertIn(b'NEW', response.content)
        self.assertIn(b'BUCKET', response.content)
        self.assertEqual(response.status_code, 200)

        # post with setting key/no bucket parameter, Setting value changed
        request = self.factory.post(
            'admin/dynsettings/setting/edit',
            {self.setting: 'NEW'}
        )
        response = edit_settings(request)
        self.assertIn(b'NEW', response.content)
        self.assertIn(b'SET', response.content)
        self.assertNotIn(b'Firstval', response.content)
        self.assertEqual(response.status_code, 200)
