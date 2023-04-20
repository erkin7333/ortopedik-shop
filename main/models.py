from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
from account.models import User


class Category(TranslatableModel):
    """Kategoriyalar uchun model"""

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100, db_index=True)
    )
    image_uz = models.ImageField(upload_to='category/', blank=True, null=True)
    image_ru = models.ImageField(upload_to='category/', blank=True, null=True)

    def __str__(self):
        return f"{self.safe_translation_getter('name')}"

    class Meta:
        verbose_name = _("Category")


class BaseProduct(TranslatableModel):
    """BaseProduct model"""

    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=100, blank=True, null=True),
        title=models.CharField(_('Title'), max_length=500, blank=True, null=True),
        description=models.TextField()
    )
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    k_id = models.IntegerField()
    vendor_code = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/', blank=True)
    image1 = models.ImageField(upload_to='product/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    available_sale = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.safe_translation_getter('name')} - {self.vendor_code}"

    class Meta:
        verbose_name = _("BaseProduct")


class Products(TranslatableModel):
    """Maxsulotlar uchun model"""

    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=100, blank=True, null=True),
    )
    image = models.ImageField(upload_to="variant/", blank=True, null=True)
    baseproduct = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, blank=True, null=True)
    warehouse = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=50, verbose_name=_("Color name"))
    size = models.CharField(max_length=20, verbose_name=_("Size"))
    price = models.IntegerField(blank=True, null=True)
    k_id = models.IntegerField()
    number = models.CharField(max_length=50, verbose_name=_('Shotuv kodi'))
    p_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # def __str__(self):
    #     return f"{self.safe_translation_getter('name')}"

    def __str__(self):
        return str(self.k_id)

    class Meta:
        verbose_name = _("Product")


class Payment(models.Model):
    """To'lov tizimlari uchun"""
    name = models.CharField(max_length=50)
    payme_code = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Payment")


class Province(models.Model):
    """Viloyatlar nomlari uchun"""

    name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Viloyat nomi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Province")


class Delivery(TranslatableModel):
    """Yetkaziberish turlari uchun"""

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100, db_index=True)
    )
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.safe_translation_getter('name')}"


class Order(models.Model):
    """Zakazlar uchun"""

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    payment_type = models.ForeignKey(Payment, on_delete=models.RESTRICT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=18)
    phone1 = models.CharField(max_length=18)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)
    type_of_delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, verbose_name=_("Yetkazib berish turi"))
    full_address = models.TextField()
    paid_amount = models.FloatField(blank=True, null=True, verbose_name=_("Umumiy maxsulot narxi"))
    is_paid = models.FloatField(blank=True, null=True, verbose_name=_("Jami narx"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _("Order")


class OrderItem(models.Model):
    """Har bir zakaz uchun"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.RESTRICT, related_name='items')
    warehouse = models.IntegerField(blank=True, null=True)
    number = models.CharField(max_length=8)
    size = models.CharField(max_length=10)
    price_per_product = models.FloatField()
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField()

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = _("OrderItem")
