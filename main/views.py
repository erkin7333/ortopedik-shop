from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from main.cart import Cart
from .models import Products, OrderItem, Order
from .forms import AddProductForm, OrderModelForm
from click.models import ClickOrders
from payment.models import PaymentOrder
import requests
from config import settings
from django.db.models import Q
from datetime import datetime



class NewProduct(ListView):
    """Glavni saxifaga maxsulotlarnii chiqarish"""

    model = Products
    template_name = 'main/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Products.objects.filter(p_quantity__gt=0).order_by('-id')


class CategoryProductListView(ListView):
    """Mahsulotlarni kategoriya bo'yicha filter qilish """

    template_name = "main/category-product.html"
    model = Products
    context_object_name = 'posts'
    paginate_by = 3
    def get_queryset(self):
        return Products.objects.filter(p_quantity__gt=0, categories_id=self.kwargs['pk'])


class ProductListView(ListView):
    """Peoductlarni ko'rish uchun Class based views"""

    template_name = "main/product.html"
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Products.objects.filter(p_quantity__gt=0).order_by('-id')



class SearchResultView(ListView):
    """Maxsulotlarni izlash uchun CLass"""

    model = Products
    template_name = "main/search.html"

    def get_queryset(self):
        query =self.request.GET.get('query')
        object_list = Products.objects.filter(Q(translations__name__icontains=query), Q(translations__title__icontains=query))
        return object_list



def productdetails(request, product_id):
    """Maxsulotni tavsilotini ko'rish uchun funksiya"""

    cart = Cart(request)
    details = Products.objects.filter(id=product_id)
    single = Products.objects.get(id=product_id)
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            color = form.data.get('color', None)
            size = form.data.get('size', None)
            cart.add(product_id=single.id, color=color, size=size, number=single.number,
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
                number = item['number']
                warehouse = item['warehouse']
                size = item['size']
                color = item['color']
                p_k_id = product.k_id
                print("FFFFFFFFFFFFFFFFFFFFFFf======", p_k_id)
                unit_price = item['price']
                price = product.price * quantity
                order_item = OrderItem(order=order, product=product, quantity=quantity,
                                       number=number, total_price=price, size=size,
                                       color=color, price_per_product=unit_price, warehouse=warehouse)
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
                    "items": [
                        {
                            "product": {
                                "id": product.k_id,
                                "code": item['number']
                            },
                            "quantity": item['quantity'],
                            "unitPrice": item['price'],
                            "warehouseId": item['warehouse']
                        } for item in cart
                    ],
                    "payments": [
                        {
                            "account": {
                                "id": order.payment_type.payme_code
                            },
                            "amount": order.paid_amount,
                            "date": datetime.now().strftime('%Y-%m-%d'),
                        }
                    ],
                    "status": "APPROVE"
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
            if order.payment_type.payme_code == 249:
                print("PPPPPPPPPPPPPPPPPPPP", order.payment_type.payme_code)
                return redirect('payment:payme')
            else:
                print("CCCCCCCCCCCCCCCCCCCCCCCC", order.payment_type.payme_code)
                return redirect("click:getclick")

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
