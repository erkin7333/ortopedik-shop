from django.urls import path
from .views import *

app_name = "click"

urlpatterns = [
    path('initialize_payment/', initialize_payment_api_view, name='initialize_payment'), # Complete URL (Адрес результата) ga qo'yasiz.
    path('integration_with_click/', accept_click_request_view, name='integration_with_click'), # Prepare URL (Адрес проверки) ga qo'yasiz.
    path('getclick/', clickget, name='getclick'),
    # path('create_click_order/', create_click_order, name="create_click_order")
]
