from django import forms
from .models import ContactUs
from django.utils.translation import gettext_lazy as _


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'  # show all fields
        exclude = ['response', 'is_read_by_admin', 'upload']  # not show response
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('name'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('email'),
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('subject'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('message'),
            }),
            'upload': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': _('uploads'),
                'name': 'image',
                'accept': "image/*",  # not working
            }),

        }
        labels = {
            'name': 'Name'
        }
        error_messages = {
            'name': {
                'required': _('please enter your name')
            }
        }
