# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import template

from dynsettings.models import SettingCache


register = template.Library()


@register.simple_tag
def get_dynsetting(key, bucket=None):
    return SettingCache.get_value_object(key)(bucket)
