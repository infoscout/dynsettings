from __future__ import absolute_import
from django import template
from dynsettings.models import SettingCache

register = template.Library()


@register.assignment_tag
def get_dynsetting(key, bucket=None):
    return SettingCache.valuedict[key](bucket)

