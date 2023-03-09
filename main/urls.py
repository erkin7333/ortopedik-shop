from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = [
    path('', NewProduct.as_view(), name='home'),

    path('product/', ProductListView.as_view(), name='product'),

    path('p-detail/<int:product_id>/', productdetails, name='p_detail'),

    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('change_quantity/<int:product_id>/', change_quantity, name='change_quantity'),

    path('addtocart/', addtocart, name='addtocart'),

    path('remove-cart/<int:product_id>/', remove_cart, name='remove_cart'),

    path('checkout/', checkout, name='chekout'),

    path('payment/', payment_method, name="payment")
]