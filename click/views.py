import decimal
from decimal import Decimal
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz
from django.conf import settings
from .helper import CheckClickTransaction
from .service import initialize_transaction
from .models import TRANSACTIONTYPECHOICES, ClickOrders
from . import serializers
from rest_framework import permissions
from django.shortcuts import redirect
from django.views import View
from main.models import Order
from .forms import ClickOrdersForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

converter_amount_click = settings.CLICK_PRICE_HELPER


class InitializePaymentAPIView(APIView):
    serializer_class = serializers.InitializePaymentSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        transaction_type = data.validated_data.get("transaction_type")
        price = data.validated_data.get("price")

        transaction_id = initialize_transaction(
            request.user,
            price,
            transaction_type,
        )
        generated_link = ""
        if transaction_type == TRANSACTIONTYPECHOICES.CLICK:
            price = price * converter_amount_click
            generated_link = ClickUz.generate_url(
                order_id=transaction_id,
                amount=price
            )
        return Response(
            status=status.HTTP_200_OK,
            data={"generated_link": generated_link},
        )


initialize_payment_api_view = InitializePaymentAPIView.as_view()


class AcceptClickRequestsView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = CheckClickTransaction


accept_click_request_view = AcceptClickRequestsView.as_view()



def clickget(request):
    user = request.user
    click_p = Order.objects.filter(user=user).last()
    if request.method == 'POST':
        transaction_type = request.POST.get('transaction_type[]')
        print("TYPE=======", transaction_type)
        amount = request.POST.get('amount[]')
        print("AMOUNT=======", amount)
        user = request.user
        amount_decimal = Decimal(amount.replace(',', '.'))
        price = amount_decimal * converter_amount_click
        print("YUYTRYUYT====", type(price))
        order = ClickOrders.objects.create(user=user, amount=int(price), transaction_type=transaction_type)
        generated_link = ClickUz.generate_url(order_id=order.id, amount=price)
        print("URL GENERET=====", generated_link)
        return redirect(generated_link)
    return render(request, 'main/click.html', {"click_p": click_p})
