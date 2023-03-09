from django.contrib import admin
from .models import Category, Products, Color, ProductSize, Payment, Order, OrderItem
from parler.admin import TranslatableAdmin


admin.site.register(Color)
admin.site.register(ProductSize)


class CategoryAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'image')
    list_display_links = ('name',)

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(TranslatableAdmin):
    list_display = ('id', 'k_id', 'categories', 'name', 'price', 'p_quantity', 'number', 'created_at')
    list_display_links = ('name', 'k_id')
    list_per_page = 687
    search_fields = ['number', 'k_id']

admin.site.register(Products, ProductAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'payme_code')
    list_display_links = ('id', 'name')

admin.site.register(Payment, PaymentAdmin)



class OrderItemIneLineAdmin(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemIneLineAdmin]

admin.site.register(Order, OrderAdmin)


