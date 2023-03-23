from django.urls import path

from payment.views import *

app_name = "payment"

urlpatterns = [
    path('', payment_method, name="payme"),
]