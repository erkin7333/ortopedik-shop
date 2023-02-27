from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from main.cart import Cart
from .models import Product, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import AddProductForm, OrderModelForm
import requests
from config import settings

class NewProduct(ListView):
    """Glavni saxifaga maxsulotlarnii chiqarish"""

    model = Product
    template_name = 'main/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        code = {
            "limit": 10,
            "start": 0
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=UTF-8",
            "accessToken": settings.ACCESS_TOKEN,
            "x-auth": settings.X_TOKEN
        }
        response = requests.post("https://apps.kpi.com/services/api/v2/2/products_zapier", json=code, headers=headers)
        api_products = response.json()
        api_vendor_codes = [p['number'] for p in api_products]
        return Product.objects.filter(vendor_code__in=api_vendor_codes).order_by('-id')


class ProductListView(ListView):
    """Peoductlarni ko'rish uchun Class based views"""

    template_name = "main/product.html"
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        code = {
            "limit": 10,
            "start": 0
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=UTF-8",
            "accessToken": settings.ACCESS_TOKEN,
            "x-auth": settings.X_TOKEN
        }
        response = requests.post("https://apps.kpi.com/services/api/v2/2/products_zapier", json=code, headers=headers)
        api_products = response.json()
        api_vendor_codes = [p['number'] for p in api_products]
        return Product.objects.filter(vendor_code__in=api_vendor_codes).order_by('-id')


def productdetails(request, product_id):
    """Maxsulotni tavsilotini ko'rish uchun funksiya"""

    cart = Cart(request)
    details = Product.objects.filter(id=product_id)
    single = Product.objects.get(id=product_id)
    print("SSSSSSSSSSSSSSSSSSs", single.vendor_code)
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            color = form.data.get('color', None)
            size = form.data.get('size', None)
            print("COLOR, SIZE ==============================", color, size)
            cart.add(product_id=single.id, color=color, size=size, vendor_code=single.vendor_code,
                     price=single.price)
            return redirect('main:addtocart')
    else:
        form = AddProductForm(request.POST)
    context = {
        'form': form,
        'details': details,
    }
    return render(request, 'main/detaile.html', context=context)


def add_to_cart(request, product_id):
    """Mahsulotni sotib olish funktsiyasi"""
    cart = Cart(request)
    cart.add(product_id)
    return redirect('main:addtocart')


def change_quantity(request, product_id):
    """Maxsulot soninii o'zgartirish uchun funksiya"""

    action = request.GET.get('action', '')
    if action:
        quantity = 1
        if action == 'decrease':
            quantity = -1
        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect("main:addtocart")


def remove_cart(request, product_id):
    """Kardagi maxsulotni o'chirish uchun funksiya"""

    cart = Cart(request)
    cart.remove(str(product_id))
    return redirect('main:addtocart')

def addtocart(request):
    cart = Cart(request)
    my_data = request.session.get('cart')

    return render(request, 'main/cart.html', {'cart': cart, 'my_data': my_data})

def chekout(request):
    """Checkout qismi uchun funksiya"""

    cart = Cart(request)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            total_price = 0
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                total_price += product.price * quantity
            order = form.save(commit=False)
            order.user = request.user
            order.paid_amount = total_price
            order.save()
            for item in cart:
                product = item['product']
                print("ORDER99999999999999999999999999999999", product)
                vendor_code = item['vendor_code']
                size = item['size']
                color = item['color']
                quantity = item['quantity']
                prices = item['price']
                price = product.price * quantity
                item = OrderItem.objects.create(order=order, product=product, quantity=quantity, vendor_code=vendor_code,
                                                total_price=price, size=size, color=color, price_per_product=prices)
                item.save()
            cart.clear()
        return redirect('main:home')

    else:
        form = OrderModelForm()
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'main/checkout.html', context=context)
