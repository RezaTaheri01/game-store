from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("name"))
    email = models.EmailField(max_length=300, verbose_name=_('email'))
    subject = models.CharField(max_length=300, verbose_name=_("title"))
    message = models.TextField(verbose_name=_('message'))
    created_date = models.DateTimeField(verbose_name=_("send date"), auto_now_add=True)
    response = models.TextField(verbose_name=_('answer'), null=True, blank=True)
    is_read_by_admin = models.BooleanField(default=False, verbose_name=_('read by admin'))

    # upload = models.ImageField(verbose_name='خوانده شده', null=True, upload_to='images')

    class Meta:
        verbose_name = _('contact us list')
        verbose_name_plural = _('contact us list')

    def __str__(self):
        return self.subject
