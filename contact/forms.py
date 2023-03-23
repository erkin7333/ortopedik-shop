from django import forms
from .models import Requestforhelp
from django.utils.translation import gettext_lazy as _


class RequestforhelpForm(forms.ModelForm):
    """Yordam va takliflar uchun forma"""

    class Meta:
        model = Requestforhelp
        fields = ('full_name', 'email', 'phone', 'company', 'description')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': _('F.I.O')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': _('Email')
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': '+99890 123-45-67'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': _('Kompaniya')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'type': 'text',
                'rows': '3',
                'placeholder': _('Xabar')
            })
        }