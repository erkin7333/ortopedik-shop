from django import forms
from .models import Requestforhelp



class RequestforhelpForm(forms.ModelForm):
    """Yordam va takliflar uchun forma"""

    class Meta:
        model = Requestforhelp
        fields = ('full_name', 'email', 'phone', 'company', 'description')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'F.I.O'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': '+99890 123-45-67'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Company'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'type': 'text',
                'rows': '3',
                'placeholder': 'Message'
            })
        }