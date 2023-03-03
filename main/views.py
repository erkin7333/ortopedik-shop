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
from datetime import datetime
from django.core.cache import cache
import asyncio
import aiohttp
import threading


class NewProduct(ListView):
    """Glavni saxifaga maxsulotlarnii chiqarish"""

    model = Product
    template_name = 'main/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        code = {
            "limit": 5,
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
            "limit": 5,
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
        kpi_id = [s['id'] for s in api_products]
        return Product.objects.filter(vendor_code__in=api_vendor_codes).order_by('-id')



async def get_api_date(limit=1000, strat=0):
    """API dan ma'lumotlarni olish uchun async funktsiyasi"""

    code = {
        "limit": limit,
        "start": strat
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "accessToken": settings.ACCESS_TOKEN,
        "x-auth": settings.X_TOKEN
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f"https://apps.kpi.com/services/api/v2/2/products/", json=code) as response:
            api_product = await response.json()
    return api_product


def productdetails(request, product_id):
    """Maxsulotni tavsilotini ko'rish uchun funksiya"""

    cart = Cart(request)
    details = Product.objects.filter(id=product_id)
    single = Product.objects.get(id=product_id)
    api_product = cache.get('api_product')
    if not api_product:
        api_product = asyncio.run(get_api_date())
        cache.set('api_product', api_product, 3600)
    api_quantitys = api_product.get('data', {}).get('list')
    api_vendor_codes = [p['number'] for p in api_quantitys]
    quantity_api = [q['quantity'] for q in api_quantitys]
    print("MAXSULOT SONI ===============", len(api_vendor_codes))
    print("SOTUVDA NECHTADAN BORLARI  ===============", quantity_api)
    print("SOTUV KODI ==================", api_vendor_codes)
    if single.vendor_code in api_vendor_codes:
        index = api_vendor_codes.index(single.vendor_code)
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            color = form.data.get('color', None)
            size = form.data.get('size', None)
            cart.add(product_id=single.id, color=color, size=size, vendor_code=single.vendor_code,
                     price=single.price)
            return redirect('main:addtocart')
    else:
        form = AddProductForm(request.POST)
    context = {
        'form': form,
        'details': details,
        'api_quantity': api_quantitys[index]['quantity']
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


import threading

def checkout(request):
    """Hisob-kitob bo'limi uchun funksiya"""

    cart = Cart(request)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            total_price = 0
            order_items = []
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
                quantity = item['quantity']
                total_price += product.price * quantity
                vendor_code = item['vendor_code']
                size = item['size']
                color = item['color']
                unit_price = item['price']
                price = product.price * quantity
                order_item = OrderItem(order=order, product=product, quantity=quantity,
                                       vendor_code=vendor_code, total_price=price, size=size,
                                       color=color, price_per_product=unit_price)
                order_items.append(order_item)
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            OrderItem.objects.bulk_create(order_items)
            cart.clear()

            # API so'rovini asinxron tarzda qilindi
            def make_api_request():
                api_url = "https://apps.kpi.com/services/api/v3/sales/invoice"
                order_invoice = {
                    "customer": {
                        "id": request.user.kpi_id
                    },
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "dueDate": datetime.now().strftime('%Y-%m-%d'),
                    "status": "APPROVE",
                    "items": [
                        {
                            "product": {
                                "code": item['vendor_code']
                            },
                            "quantity": item['quantity'],
                            "unitPrice": item['price']
                        } for item in cart
                    ]
                }
                print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDD", order_invoice)
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "accessToken": settings.ACCESS_TOKEN,
                    "x-auth": settings.X_TOKEN
                }
                response = requests.post(api_url, json=order_invoice, headers=headers,)
                data_json = response.json()
                print("INVOICE=========", data_json)
                if response.status_code == 200:
                    data_json = response.json()
                    print("INVOICE=========", data_json)

            threads = []
            thread = threading.Thread(target=make_api_request)
            print("TTTTTTTTTTTTTTTTTTTTTTTT", thread)
            threads.append(thread)
            thread.start()

            return redirect('main:home')

    else:
        form = OrderModelForm()
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'main/checkout.html', context=context)





# def checkout(request):
#     """Checkout qismi uchun funksiya"""
#
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderModelForm(request.POST)
#         if form.is_valid():
#             total_price = 0
#             for item in cart:
#                 product = item['product']
#                 quantity = item['quantity']
#                 total_price += product.price * quantity
#             order = form.save(commit=False)
#             order.user = request.user
#             order.paid_amount = total_price
#             order.save()
#             for item in cart:
#                 product = item['product']
#                 vendor_code = item['vendor_code']
#                 size = item['size']
#                 color = item['color']
#                 quantity = item['quantity']
#                 unit_price = item['price']
#                 user_kpi = request.user.kpi_id
#                 date = datetime.now().isoformat()
#                 price = product.price * quantity
#                 item = OrderItem.objects.create(order=order, product=product, quantity=quantity,
#                                                 vendor_code=vendor_code,
#                                                 total_price=price, size=size, color=color,
#                                                 price_per_product=unit_price)
#                 api_url = "https://apps.kpi.com/services/api/v3/sales/invoice"
#                 order_invoice = {
#                     "customer": {
#                         "id": user_kpi
#                     },
#                     "date": date,
#                     "dueDate": date,
#                     "status": "APPROVE",
#                     "items": [
#                         {
#                             "product": {
#                                 "code": vendor_code
#                             },
#                             "quantity": quantity,
#                             "unitPrice": unit_price
#                         }
#                     ]
#                 }
#                 print("API ga post buladigan malumotlar=======", order_invoice)
#                 headers = {
#                     "Content-Type": "application/json",
#                     "Accept": "application/json",
#                     "accessToken": settings.ACCESS_TOKEN,
#                     "x-auth": settings.X_TOKEN
#                 }
#                 response = requests.post(api_url, json=order_invoice, headers=headers,)
#                 if response.status_code == 200:
#                     data_json = response.json()
#                     print("INVOICE=========", data_json)
#                 item.save()
#             cart.clear()
#         return redirect('main:home')
#
#     else:
#         form = OrderModelForm()
#     context = {
#         'cart': cart,
#         'form': form
#     }
#     return render(request, 'main/checkout.html', context=context)
