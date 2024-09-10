from django.contrib.auth.models import AbstractUser, AbstractBaseUser  # بیس کار فقط
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


# Create your models here.

class User(AbstractUser):  # way 2 plus normal fields (AbstractUser)
    email = models.EmailField(_("email address"))
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    about_user = models.TextField(null=True, blank=True, verbose_name=_("about user"))
    country_code = models.CharField(max_length=10, verbose_name=_("area code"), null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name=_("Phone Number"), null=True, blank=True)
    telephone_number = models.CharField(max_length=15, verbose_name=_("Telephone Number"), null=True, blank=True)
    email_active_code = models.CharField(max_length=108, verbose_name=_("Active Code"), null=True, blank=True,
                                         default=get_random_string(72))
    address = models.TextField(max_length=108, verbose_name=_("Address"), null=True, blank=True)
    profile_image = models.ImageField(upload_to='images/profile', null=True, verbose_name=_("Profile Picture"),
                                      blank=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    #
    def __str__(self):
        return self.username
