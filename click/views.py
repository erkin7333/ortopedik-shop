from django.shortcuts import render, redirect
from .models import ClickOrder
from pyclick import PyClick
from pyclick.views import PyClickMerchantAPIView
from rest_framework.generics import CreateAPIView


class CreateClickOrderView(CreateAPIView):

    def get(self, request, *args, **kwargs):
        order = ClickOrder.objects.filter(user=request.user).last()
        return_url = 'http://127.0.0.1:8000/'
        url = PyClick.generate_url(order_id=order.id, amount=str(order.amount), return_url=return_url)
        print("CLICK===============", url)
        return redirect(url)


def click_method(request):
    click_p = ClickOrder.objects.filter(user=request.user).last()
    return_url = "http://127.0.0.1:8000/"
    url = PyClick.generate_url(order_id=click_p.id, amount=str(click_p.amount), return_url=return_url)
    print("FFFFFFFF===", url)
    context = {
        'click_p': click_p,
        'url': url
    }
    return render(request, 'main/click.html', context=context)


class OrderCheckAndPayment(PyClick):
    def check_order(self, order_id: str, amount: str):
        if order_id:
            try:
                order = ClickOrder.objects.get(id=order_id)
                if int(amount) == order.amount:
                    return self.ORDER_FOUND
                else:
                    return self.INVALID_AMOUNT
            except ClickOrder.DoesNotExist:
                return self.ORDER_NOT_FOUND

    def successfully_payment(self, order_id: str, transaction: object):

        try:
            order = ClickOrder.objects.get(id=order_id)
            order.is_paid = True
            order.save()
        except ClickOrder.DoesNotExist:
            print(f"hech qanday buyurtma ob'ekti topilmadi: {order_id}")

class OrderTestView(PyClickMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment
