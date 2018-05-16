# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render

from dynsettings.admin.forms import BucketsForm
from dynsettings.models import Bucket, BucketSetting, Setting


def bucket_setting_create(val, setting, bucket):
    # save bucket setting from edit_settings
    if val:
        bucket_setting, created = BucketSetting.objects.get_or_create(
            bucket=bucket,
            setting=setting
        )

        bucket_setting.value = val
        bucket_setting.full_clean()
        bucket_setting.save()


def edit_settings(request):
    # Get all settings
    qs = Setting.objects.order_by("key")
    if request.GET.get('search'):
        qs = qs.filter(key__icontains=request.GET['search'])
    settings = qs.all()

    # Get bucket
    bucket = None
    if request.GET.get('bucket'):
        bucket = Bucket.objects.get(pk=request.GET['bucket'])

    buckets_form = BucketsForm(request.GET)

    # Save updates to db
    if request.method == 'POST':
        for setting in settings:
            val = request.POST.get(setting.key)
            # Save bucket setting
            if bucket:
                bucket_setting_create(val, setting, bucket)
            else:
                setting.value = val
                setting.full_clean()
                setting.save()

        # Redirect to self
        messages.info(
            request,
            (
                "Settings have been saved. Need to restart apache for settings"
                " to take full effect!"
            )
        )
    # Get bucket settings
    bucket_settings = {}
    if bucket:
        bucket_settings = BucketSetting.objects.filter(bucket=bucket)

        # Change to dict for lookup
        bucket_settings = dict([(s.setting.key, s,) for s in bucket_settings])

    # Create joint tuple list (settings, bucket_settings) for template
    settings_list = []
    for setting in settings:
        settings_list.append(
                (setting, bucket_settings.get(setting.key),)
        )

    context = {'bucket': bucket,
               'settings_list': settings_list,
               'buckets_form': buckets_form,
               }

    return render(request, 'admin/dynsettings/setting/edit.html', context)
