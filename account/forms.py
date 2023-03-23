from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from .models import User
from config.validators import PhoneValidators
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.Form):
    """Registratsiya uchun forma"""

    username = forms.CharField(max_length=50, required=True, label=_("Foydalanuvchi nomi"),
                               widget=forms.TextInput(attrs={'placeholder': _('Foydalanuvchi nomi')}))
    phone = forms.CharField(max_length=20, required=True, label=_("Telefon raqam"), validators=[PhoneValidators()],
                            widget=forms.TextInput(attrs={'placeholder': _('Telefon raqam')}))
    password = forms.CharField(max_length=20, label=_("Parol"),
                               widget=forms.PasswordInput(attrs={'placeholder': _('Parol')}), required=True,
                               validators=[MinLengthValidator(3), MaxLengthValidator(10)])
    confirm = forms.CharField(max_length=20, label=_("Parolni qayta kiriting"),
                              widget=forms.PasswordInput(attrs={'placeholder': _("Parolni tasdiqlang")}),
                               required=True,
                               validators=[MinLengthValidator(3), MaxLengthValidator(10)])

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            raise ValidationError(_("Ushbu foydalanuvchi nomi bilan ro'yxatdan o'tilgan"))
        return self.cleaned_data['username']

    def clean_phone(self):
        if User.objects.filter(phone=self.cleaned_data.get('phone')).exists():
            raise ValidationError(_("Ushbu telefon raqami bilan ro'yxatdan o'tilgan"))
        return self.cleaned_data['phone']

    def clean_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise ValidationError(_('Iltimos parollar bir xilligini tekshiring'))
        return self.cleaned_data['confirm']


class LoginForm(forms.Form):
    """Tizimga kirish uchun forma"""

    username = forms.CharField(max_length=50, label=_("Foydalanuvchi nomi"),
                               widget=forms.TextInput(attrs={'placeholder': _('Foydalanuvchi nomi')}))
    password = forms.CharField(max_length=50, label=_("Parol"),
                               widget=forms.PasswordInput(attrs={'placeholder': _('Parol')}))









