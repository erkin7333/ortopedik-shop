from django.contrib import admin
from .models import Category, Products, Payment, Order, OrderItem, Delivery, Province, BaseProduct
from parler.admin import TranslatableAdmin

admin.site.register(Province)


class CategoryAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'image_uz', 'image_ru')
    list_display_links = ('name',)


admin.site.register(Category, CategoryAdmin)


class BaseProductAdmin(TranslatableAdmin):
    list_display = ("id", "k_id", "name")
    list_display_links = ("id", "k_id", "name")
    list_per_page = 687
    search_fields = ['vendor_code', 'k_id']


admin.site.register(BaseProduct, BaseProductAdmin)


class ProductAdmin(TranslatableAdmin):
    list_display = ('id', 'k_id', 'name', 'price', 'p_quantity', 'number', 'created_at')
    list_display_links = ('name', 'number', 'k_id')
    list_per_page = 687
    search_fields = ['number', 'k_id']


admin.site.register(Products, ProductAdmin)


class DeliveryAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'price')
    list_display_links = ('id', 'name')


admin.site.register(Delivery, DeliveryAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'payme_code')
    list_display_links = ('id', 'name')


admin.site.register(Payment, PaymentAdmin)


class OrderItemIneLineAdmin(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemIneLineAdmin]


admin.site.register(Order, OrderAdmin)
