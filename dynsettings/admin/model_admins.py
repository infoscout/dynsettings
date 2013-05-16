from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from infoscout.apps.dynsettings.models import BucketSetting
from infoscout.apps.dynsettings.admin.views import edit_settings


class BucketSettingInline(admin.TabularInline):
    model = BucketSetting


class SettingAdmin(admin.ModelAdmin):
    
    # Changelist files
    list_display = ('key','value', 'help_text','data_type')
    list_editable = ('value',)
    #linked_display_links = ()
    
    fields = ('key','value','data_type',)
    readonly_fields = ('key','help_text','data_type')
    search_fields = ('key',)
    ordering = ('key',)
    actions = []
    
    inlines = [BucketSettingInline]
    
    def key(self, obj):
        return obj.key
    
    def has_add_permission(self, request):
        return False
    
    def get_urls(self):
        urls = super(SettingAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^edit/?$', self.admin_site.admin_view(edit_settings), name='dynsettings_setting_edit'),  
        )
        return my_urls + urls
    
    
class BucketAdmin(admin.ModelAdmin):
    list_display = ('key','bucket_type','probability','desc')
    list_editable = ('probability',)
    ordering = ('key',)
    
    pass    
