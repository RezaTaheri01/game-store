from django.contrib import admin
from .models import ContactUs
from utils import email_service
from django.utils.translation import gettext_lazy as _


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ['name',
                       'email',
                       'subject',
                       'message',
                       'created_date',
                       'is_read_by_admin', ]
    list_display = ['__str__', 'is_read_by_admin', 'created_date']
    list_filter = ['is_read_by_admin', 'created_date']
    ordering = ['is_read_by_admin']

    # list_editable = ['is_read_by_admin']

    def save_model(self, request, obj, form, change):
        mail = obj.email
        response_message = obj.response
        user_message = obj.message
        is_read = obj.is_read_by_admin
        if not is_read and response_message != '':
            email_service.send_email(_('reply to your message'), mail, 'email/response.html',
                                     {'user_message': user_message, 'response_message': response_message})
            obj.is_read_by_admin = True
            obj.save()


admin.site.register(ContactUs, ContactAdmin)
