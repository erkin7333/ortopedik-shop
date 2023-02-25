from django.contrib import admin
from .models import Category, Product, Color, ProductSize, Payment, Order, OrderItem
from parler.admin import TranslatableAdmin

class CategoryAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'image')
    list_display_links = ('name',)

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(TranslatableAdmin):
    list_display = ('id', 'categories', 'name', 'title',
                    'description', 'price', 'vendor_code',
                    'image', 'image1', 'image2', 'image3', 'created_at')
    list_display_links = ('name', 'title')
    list_per_page = 5
    search_fields = ('name', 'vendor_code')

admin.site.register(Product, ProductAdmin)

admin.site.register(Color)
admin.site.register(ProductSize)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

admin.site.register(Payment, PaymentAdmin)



class OrderItemIneLineAdmin(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemIneLineAdmin]

admin.site.register(Order, OrderAdmin)

