from django.contrib import admin
from . import models


# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'is_superuser', 'is_staff', 'is_active']
    list_editable = ['is_staff']


admin.site.register(models.User, AccountAdmin)
