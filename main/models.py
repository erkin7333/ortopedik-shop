from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
from account.models import User



class Category(TranslatableModel):
    """Kategoriyalar uchun model"""

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100, db_index=True)
    )
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    def __str__(self):
        return f"{self.safe_translation_getter('name')}"

    class Meta:
        verbose_name = _("Category")


class Product(TranslatableModel):
    """Maxsulotlar uchun model"""

    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ManyToManyField('Color', related_name='colors')
    size = models.ManyToManyField('ProductSize', related_name='product_size')
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=100),
        title=models.CharField(_('Title'), max_length=500),
        description=models.TextField()
    )
    price = models.IntegerField()
    vendor_code = models.CharField(max_length=10, verbose_name=_('Shotuv kodi'))
    image = models.ImageField(upload_to='product/')
    image1 = models.ImageField(upload_to='product/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.safe_translation_getter('name')}"

    class Meta:
        verbose_name = _("Product")


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Color name"))
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Color")

class ProductSize(models.Model):
    size = models.CharField(max_length=20, verbose_name=_("Size"))
    def __str__(self):
        return self.size
    class Meta:
        verbose_name = _("ProductSize")


class Payment(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _("Payment")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    payment_type = models.ForeignKey(Payment, on_delete=models.RESTRICT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    full_address = models.TextField()
    paid_amount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _("Order")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='items')
    vendor_code = models.CharField(max_length=8)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=30)
    price_per_product = models.FloatField()
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField()



    def __str__(self):
        return str(self.order)
    class Meta:
        verbose_name = _("OrderItem")




