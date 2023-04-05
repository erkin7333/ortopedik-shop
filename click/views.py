from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from . import serializers
from .methods_merchant_api import Services
from .models import ClickOrder
from .status import (ORDER_FOUND, INVALID_AMOUNT, ORDER_NOT_FOUND)
from .utils import PyClickMerchantAPIView


class CreateClickTransactionView(CreateAPIView):

    def get(self, request, *args, **kwargs):
        order = ClickOrder.objects.filter(user=request.user).last()
        return_url = 'https://makonmirzo.uz/'
        url = PyClickMerchantAPIView.generate_url(order_id=order.id, amount=str(order.amount), return_url=return_url)
        print("CLICK===============", url)
        return redirect(url)


class TransactionCheck(PyClickMerchantAPIView):
    @classmethod
    def check_order(cls, order_id: str, amount: str):
        if order_id:
            try:
                order = ClickOrder.objects.get(id=order_id)
                if int(amount) == order.amount:
                    return ORDER_FOUND
                else:
                    return INVALID_AMOUNT
            except ClickOrder.DoesNotExist:
                return ORDER_NOT_FOUND

    @classmethod
    def successfully_payment(cls, transaction: ClickOrder):
        """ Эта функция вызывается после успешной оплаты """
        pass


class ClickTransactionTestView(PyClickMerchantAPIView):
    VALIDATE_CLASS = TransactionCheck


class ClickMerchantServiceView(APIView):
    def post(self, request, service_type, *args, **kwargs):
        service = Services(request.POST, service_type)
        response = service.api()
        return JsonResponse(response)