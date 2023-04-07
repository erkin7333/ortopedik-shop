from django.db import models
from account.models import User
from django.utils.translation import gettext_lazy as _




class TRANSACTIONTYPECHOICES(models.TextChoices):
    CLICK = "click"


class TRANSACTIONSTATUS(models.TextChoices):
    NEW = "new"
    VERIFIED = "verified"
    PAID = "paid"
    CANCELED = "canceled"

class ClickOrder(models.Model):
    """ Класс ClickTransaction """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name=_("To'lov miqdori (so'mda)"), max_digits=9, decimal_places=2,
                                 default="0.0")
    transaction_external_id = models.CharField(max_length=30, blank=True, default="")
    is_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTIONTYPECHOICES.choices)
    status = models.CharField(max_length=10, choices=TRANSACTIONSTATUS.choices, default=TRANSACTIONSTATUS.NEW)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = "ClickOrder"
        verbose_name_plural = "ClickOrders"

    def verify(self):
        self.status = TRANSACTIONSTATUS.VERIFIED
        self.is_verified = True
        self.save()

    def make_payment(self):
        self.status = TRANSACTIONSTATUS.PAID
        self.is_paid = True
        self.save()

    def cancel(self):
        self.status = TRANSACTIONSTATUS.CANCELED
        self.is_canceled = True
        self.is_paid = False
        self.save()

    def __str__(self):
        return str(self.id)



