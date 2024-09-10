from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SiteModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_module'
    verbose_name = _("Site Settings")
