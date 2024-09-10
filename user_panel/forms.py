from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

from account.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'telephone_number', 'profile_image', 'address']  # show all fields
        # exclude = ['response', 'is_read_by_admin', 'upload']  # not show response
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('first name'),
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('last name'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('email'),
            }),
            'telephone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '051-41216578',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Address'),
                'row': 2,
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': _('uploads'),
                'name': 'profile_image',
                'id': 'profileImageInput',
                'hidden': True,
                'accept': "image/*",  # not working
                'onchange': "readURL(this)",
            }),

        }
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'telephone_number': _('Telephone'),
            'address': _('Address'),
        }
        error_messages = {
            'name': {
                'required': _('please enter your name')
            }
        }


class ResetPasswordInPanelForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Current Password'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(8)
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('New Password'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(8)
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm Password'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(8)
        ]
    )

    # custom validator
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError(_('password not match'))
