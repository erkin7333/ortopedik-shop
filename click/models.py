from django.db import models
from account.models import User
from django.utils.translation import gettext_lazy as _


class ClickOrder(models.Model):
    """ Класс ClickTransaction """
    PROCESSING = 'processing'
    WAITING = "waiting"
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    ERROR = 'error'

    STATUS = (
        (WAITING, WAITING),
        (PROCESSING, PROCESSING),
        (CONFIRMED, CONFIRMED),
        (CANCELED, CANCELED),
        (ERROR, ERROR)
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name=_("To'lov miqdori (so'mda)"), max_digits=9, decimal_places=2,
                                 default="0.0")
    click_paydoc_id = models.CharField(verbose_name=_("CLICK tizimidagi to'lov raqami"), max_length=255, blank=True)
    action = models.CharField(verbose_name=_("Qabul qilinadigan chora"), max_length=255, blank=True, null=True)
    status = models.CharField(verbose_name=_("Holat"), max_length=25, choices=STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    extra_data = models.TextField(blank=True, default="")
    message = models.TextField(blank=True, default="")

    def __str__(self):
        return self.click_paydoc_id

    def change_status(self, status: str, message=""):
        """
        To'lov holatini yangilaydi
        """
        self.status = status
        self.message = message
        self.save(update_fields=["status", "message"])
