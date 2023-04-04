from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz
from django.conf import settings
from .helper import CheckClickTransaction
from .service import initialize_transaction
from .models import TRANSACTIONTYPECHOICES
from . import serializers
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from .models import ClickOrder

converter_amount_click = settings.CLICK_PRICE_HELPER


class CreateClickOrderView(CreateAPIView):

    def get(self, request, *args, **kwargs):
        order = ClickOrder.objects.filter(user=request.user).last()
        return_url = 'https://makonmirzo.uz/'
        url = ClickUz.generate_url(order_id=order.id, amount=str(order.amount), return_url=return_url)
        print("CLICK===============", url)
        return redirect(url)

# class InitializePaymentAPIView(APIView):
#     serializer_class = serializers.InitializePaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request):
#         data = self.serializer_class(data=request.data)
#         data.is_valid(raise_exception=True)
#
#         transaction_type = data.validated_data.get("transaction_type")
#         print("To'lov turi=====", transaction_type)
#         price = data.validated_data.get("price")
#         print("NARXI======", price)
#
#         transaction_id = initialize_transaction(
#             request.user,
#             price,
#             transaction_type,
#         )
#         print("To'lov id si=====", transaction_id)
#         generated_link = ""
#         if transaction_type == TRANSACTIONTYPECHOICES.CLICK:
#             price = price * converter_amount_click
#             generated_link = ClickUz.generate_url(
#                 order_id=transaction_id,
#                 amount=price
#             )
#         return Response(
#             status=status.HTTP_200_OK,
#             data={"generated_link": generated_link},
#         )


initialize_payment_api_view = CreateClickOrderView.as_view()


class AcceptClickRequestsView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = CheckClickTransaction


accept_click_request_view = AcceptClickRequestsView.as_view()













# class CreateClickOrderView(CreateAPIView):
#
#     def get(self, request, *args, **kwargs):
#         order = ClickOrder.objects.filter(user=request.user).last()
#         return_url = 'https://makonmirzo.uz/'
#         url = PyClick.generate_url(order_id=order.id, amount=str(order.amount), return_url=return_url)
#         print("CLICK===============", url)
#         return redirect(url)


# def click_method(request):
#     click_p = ClickOrder.objects.filter(user=request.user).last()
#     return_url = "http://127.0.0.1:8000/"
#     url = PyClick.generate_url(order_id=click_p.id, amount=str(click_p.amount), return_url=return_url)
#     print("FFFFFFFF===", url)
#     context = {
#         'click_p': click_p,
#         'url': url
#     }
#     return render(request, 'main/click.html', context=context)


# class OrderCheckAndPayment(PyClick):
#     def check_order(self, order_id: str, amount: str):
#         if order_id:
#             try:
#                 order = ClickOrder.objects.get(id=order_id)
#                 if int(amount) == order.amount:
#                     return self.ORDER_FOUND
#                 else:
#                     return self.INVALID_AMOUNT
#             except ClickOrder.DoesNotExist:
#                 return self.ORDER_NOT_FOUND
#
#     def successfully_payment(self, order_id: str, transaction: object):
#
#         try:
#             order = ClickOrder.objects.get(id=order_id)
#             order.is_paid = True
#             order.save()
#         except ClickOrder.DoesNotExist:
#             print(f"hech qanday buyurtma ob'ekti topilmadi: {order_id}")


# class OrderTestView(PyClickMerchantAPIView):
#     VALIDATE_CLASS = OrderCheckAndPayment
