from django.shortcuts import render
# from main.models import Order

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .models import Order
from .serializers import OrderSerializer
from paycomuz.views import MerchantAPIView
from paycomuz.models import Transaction
from paycomuz import Paycom
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal


class CheckOrder(Paycom):
    """Orderni tekshirish uchun"""

    def check_order(self, amount, account, *args, **kwargs):
        order_id = int(account['order_id'])
        order = Order.objects.filter(id=order_id).first()
        if order is not None:
            if Decimal(amount) != Decimal(order.amount_for_payme):
                return self.INVALID_AMOUNT
            return self.ORDER_FOUND
        else:
            return self.ORDER_NOT_FOND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        order_id = int(transaction.order_key)

        order = Order.objects.filter(id=order_id).first()
        order.is_payed = True
        order.save()
        print("ZAKAZ=======", order)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        order_id = int(transaction.order_key)
        order = Order.objects.filter(id=order_id).first()
        order.is_payed = False
        order.save()


@api_view(["POST"])
def checkout_view(request):
    """Tekshirish uchun """
    data = request.data
    if "id" in data and 'amount' in data:
        order_id = data['id']
        amount = Decimal(data['amount'])
        if 'return_url' in data:
            return_url = data['return_url']
        else:
            return_url = "https://makonmirzo.uz/"
        paycom = Paycom()
        data['url'] = paycom.create_initialization(amount=amount, order_id=order_id, return_url=return_url)
    return Response(data)


from django.views import View
from django.http import JsonResponse


class GetStatementView(View):
    def get(self, request):
        from_timestamp = request.GET.get("from")
        to_timestamp = request.GET.get("to")
        statement = Transaction.objects.filter(created_datetime__range=[from_timestamp, to_timestamp])
        vaqt = statement.created_datetime
        print("YANA====", vaqt)
        print("NIMADUR====", statement)
        return JsonResponse(statement)


class PaymentView(MerchantAPIView):
    """Buyerda Zakazni validate qilamiz"""
    VALIDATE_CLASS = CheckOrder


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# def payment_method(request):
#     payment_p = Order.objects.filter(user=request.user).last()
#     context = {
#         'payment_p': payment_p
#     }
#     return render(request, 'main/payment.html', context=context)
