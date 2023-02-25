from django import forms
from .models import Product, Order
from django.utils.translation import gettext_lazy as _


class AddProductForm(forms.Form):
    color = forms.CharField(max_length=20)
    size = forms.CharField(max_length=20)



class OrderModelForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'payment_type',
                  'company_name', 'email', 'phone', 'full_address')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'aa-checkout-single-bill',
                'type': 'text',
                'placeholder': _('First Name')
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'aa-checkout-single-bill',
                'type': 'text',
                'placeholder': _("Last Name")
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'aa-checkout-single-bill',
                'type': 'text',
                'placeholder': _("Company name")
            }),
            'email': forms.EmailInput(attrs={
                'class': 'aa-checkout-single-bill',
                'type': 'email',
                'placeholder': _("Email Address")
            }),
            'phone': forms.TextInput(attrs={
                'class': 'aa-checkout-single-bill',
                'type': 'tel',
                'placeholder': '+998 00-000-00-00'
            }),
            'full_address': forms.Textarea(attrs={
                'class': 'aa-checkout-single-bill',
                'type': 'text',
                'cols': '8',
                'rows': '3',
                'placeholder': _("Full Address")
            }),
            'payment_type': forms.RadioSelect(attrs={
                'class': 'aa-payment-method',
                'type': 'radio'
            })
        }














