from django.db import models
from account.models import User

class PaymentOrder(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.amount)