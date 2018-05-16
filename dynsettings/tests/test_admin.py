# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from dynsettings.admin.admin import DynsettingsAdminApp
from dynsettings.admin.views import edit_settings
from dynsettings.models import Bucket


class DynsettingsAdminAppTestCase(TestCase):
    """
    Verify Admin app is working properly
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.bucket = Bucket(key='bucket')

    def test_get_urls(self):
        app_instance = DynsettingsAdminApp(self.bucket, self.site)
        urls = app_instance.get_urls()
        self.assertEqual(len(urls), 1)

    def test_get_request(self):
        request = self.factory.get('dynsettings/edit')
        response = edit_settings(request)
        self.assertIn(b'bucket', response.content)
        self.assertEqual(response.status_code, 200)
