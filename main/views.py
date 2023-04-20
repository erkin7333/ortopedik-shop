from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from main.cart import Cart
from .models import Products, OrderItem, Order, Delivery, BaseProduct
from .forms import AddProductForm, OrderModelForm
import requests
from config import settings
from django.db.models import Q
from datetime import datetime
import threading


class NewProduct(ListView):
    """Glavni saxifaga maxsulotlarnii chiqarish"""

    model = BaseProduct
    template_name = 'main/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return BaseProduct.objects.filter().order_by('-id')


class CategoryProductListView(ListView):
    """Mahsulotlarni kategoriya bo'yicha filter qilish """

    template_name = "main/category-product.html"
    model = BaseProduct
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return BaseProduct.objects.filter(categories_id=self.kwargs['pk'])


class ProductListView(ListView):
    """Peoductlarni ko'rish uchun Class based views"""

    template_name = "main/product.html"
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return BaseProduct.objects.filter().order_by('-id')


class SearchResultView(ListView):
    """Maxsulotlarni izlash uchun CLass"""

    model = BaseProduct
    template_name = "main/search.html"

    def get_queryset(self):
        query = self.request.GET.get('query')
        object_list = BaseProduct.objects.filter(
            Q(translations__name__icontains=query) | Q(translations__title__icontains=query))
        return object_list


def detailbase(request, product_id):
    """Maxsulotni tavsilotini ko'rish uchun funksiya"""

    cart = Cart(request)
    details = BaseProduct.objects.get(id=product_id)
    variants = Products.objects.filter(baseproduct_id=details.id, p_quantity__gt=0)
    if request.method == "POST":
        product_number = request.POST["product_number"]
        product_price = request.POST.get("product_price")
        product_size = request.POST.get("product_size")
        variant_id = request.POST.get("product_k_id")
        product = Products.objects.get(k_id=variant_id)
        cart.add(product_id=product.id, number=product_number, price=product_price, size=product_size, warehouse=6)
        return redirect("main:addtocart")

    context = {
        'details': details,
        "variants": variants
    }
    return render(request, 'main/detaile.html', context=context)


@login_required
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


@login_required
def addtocart(request):
    """Savatchadagi maxsulotlarni olish"""

    cart = Cart(request)
    return render(request, 'main/cart.html', {'cart': cart})


def checkout(request):
    """Hisob-kitob bo'limi uchun funksiya"""

    cart = Cart(request)
    deliveriy = Delivery.objects.all()
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
            deliver = form.cleaned_data["type_of_delivery"]
            order.user = request.user
            order.paid_amount = total_price
            order.is_paid = total_price + deliver.price
            order.save()
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                total_price += product.price * quantity
                number = item['number']
                warehouse = item['warehouse']
                size = item['size']
                unit_price = item['price']
                price = product.price * quantity
                order_item = OrderItem(order=order, product=product, quantity=quantity,
                                       number=number, total_price=price, size=size,
                                       price_per_product=unit_price, warehouse=warehouse)
                order_items.append(order_item)
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            OrderItem.objects.bulk_create(order_items)
            cart.clear()

            # API ga invois jo'natish
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
                            "warehouseId": 6,
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
                response = requests.post(api_url, json=order_invoice, headers=headers, )
                data_json = response.json()
                print("INVOICE=========", data_json)
                if response.status_code == 200:
                    data_json = response.json()
                    print("INVOICE JO'NATILDI=========", data_json)

            threads = []
            thread = threading.Thread(target=make_api_request)
            print("APIGA MALUMOT BORDI", thread)
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
        "deliveriy": deliveriy,
        'form': form
    }
    return render(request, 'main/checkout.html', context=context)
