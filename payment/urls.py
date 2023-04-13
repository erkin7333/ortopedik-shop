from django.urls import path

from payment.views import *

app_name = "payment"

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view()),
    path('detail/<str:pk>/', OrderDetailAPIView.as_view()),
    path('pay/', PaymentView.as_view()), # EndPointUrl ga shu manzilni kiritng, agar local da foydalanmoqchi bolsez, ngrok ishlating.
    path('checkout/', checkout_view),

    # path('', payment_method, name="payme"),
]
