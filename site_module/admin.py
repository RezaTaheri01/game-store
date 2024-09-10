from django.contrib import admin
from . import models


# Register your models here.
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'site_url', 'is_main_setting', 'slide_show_number']
    list_editable = ['slide_show_number']


class SlideShowsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'order_by', 'is_active', 'is_delete', 'show_order']
    list_editable = ['is_active', 'show_order']
    ordering = ['-show_order']
    raw_id_fields = ('category',)  # interesting
    readonly_fields = ['note']


class MainSlideShowAdmin(admin.ModelAdmin):
    list_display = ['id', 'all', 'order_by']
    readonly_fields = ['note']


admin.site.register(models.SiteSetting, SiteSettingAdmin)
admin.site.register(models.SlideShow, SlideShowsAdmin)
admin.site.register(models.MainSlideShow, MainSlideShowAdmin)
