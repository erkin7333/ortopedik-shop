from django import forms
from .models import ClickOrders, TRANSACTIONTYPECHOICES

class ClickOrdersForm(forms.ModelForm):
    transaction_type = forms.ChoiceField(choices=TRANSACTIONTYPECHOICES.CLICK)
    amount = forms.DecimalField(max_digits=9, decimal_places=2)
    class Meta:
        model = ClickOrders
        fields = ['transaction_type', 'amount']



