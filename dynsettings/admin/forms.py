# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import widgets

from dynsettings.models import Bucket


class BucketModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.bucket_type:
            return "%s - %s" % (obj.bucket_type, obj.key)
        else:
            return obj.key


class BucketsForm(forms.Form):
    bucket = BucketModelChoiceField(
        queryset=Bucket.objects.order_by("bucket_type", "key"),
        empty_label="--- Defaults ---"
    )
    search = forms.CharField(widget=widgets.TextInput(attrs={'size': 60}))
