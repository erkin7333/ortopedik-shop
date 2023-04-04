from django.urls import path
from click.views import *

app_name = "click"

urlpatterns = [
    path("initialize_payment/", initialize_payment_api_view, name="initialize_payment"), # Complete URL (Адрес результата) ga qo'yasiz.
    path("integration_with_click/", accept_click_request_view, name="accept_click_requests"),  # Prepare URL (Адрес проверки) ga qo'yasiz.
    # path('', click_method, name='click_p'),
    # path('click/tra///////nsaction/', OrderTestView.as_view(), name="transaction"),
    # path('uzclick/', CreateClickOrderView.as_view(), name='uzclick')
]
