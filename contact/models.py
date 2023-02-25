from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Contact(TranslatableModel):
    """Kontact uchun model"""

    translations = TranslatedFields(
        name=models.CharField(max_length=25, verbose_name=_("Sayt nomi")),
        subject=models.CharField(max_length=255, verbose_name=_("Qisqacha malumot")),
    )
    location = models.CharField(max_length=1000, verbose_name=_("Joylashuv"))
    address = models.CharField(max_length=400, verbose_name=_("Manzil"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqam"))
    email = models.CharField(max_length=100, verbose_name=_('Elektron manzil'))
    def __str__(self):
        return f"{self.safe_translation_getter('name')}"

    class Meta:
        verbose_name = _("Contact")


class Requestforhelp(models.Model):
    """Yordam uchun murojat qilish modeli"""

    full_name = models.CharField(max_length=50, verbose_name=_("F.I.O"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqam"))
    email = models.CharField(max_length=100, verbose_name=_('Elektron manzil'))
    company = models.CharField(max_length=255, verbose_name=_("Kompaniya nomi"))
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("Requestforhelp")


class Blog(TranslatableModel):
    """Blog uchun model"""

    translations = TranslatedFields(
        subject=models.CharField(max_length=100, verbose_name=_("Subject")),
        description=models.TextField(),
    )
    image = models.ImageField(upload_to='blog/')
    def __str__(self):
        return f"{self.safe_translation_getter('subject')}"

    class Meta:
        verbose_name = _("Blog")