from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField, CaptchaTextInput
# from django_recaptcha.fields import ReCaptchaField
# from django_recaptcha.widgets import ReCaptchaV2Checkbox, ReCaptchaBase


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('username'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(6),
        ]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Email'),
        }),
        validators=[
            MaxLengthValidator(64),
            EmailValidator,
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Password'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(8)
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Confirm Password'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(8)
        ]
    )
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
        'class': 'form-control form-control-lg w-25',
    }))

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    # custom validator
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError(_('password not match'))


class SignInForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email/Username'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(6)
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(8)
        ]
    )
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
        'class': 'form-control form-control-lg w-25',
    }))


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(6)
        ]
    )
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
        'class': 'form-control form-control-lg w-25',
    }))


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
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
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
        'class': 'form-control form-control-lg w-25',
    }))

    # custom validator
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError(_('password not match'))


class ActivationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email'),
        }),
        validators=[
            MaxLengthValidator(64),
            MinLengthValidator(6)
        ]
    )
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
        'class': 'form-control form-control-lg w-25',
    }))
