from django.urls import path
from .views import *

app_name = "click"

urlpatterns = [
    path('process/click/transaction/create/', CreateClickTransactionView.as_view(), name="clicktransaction"),
    path('process/click/transaction/', ClickTransactionTestView.as_view()),
    path('process/click/service/<service_type>', ClickMerchantServiceView.as_view())
]
