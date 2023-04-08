from .models import ClickOrders
from clickuz import ClickUz
from decimal import Decimal


class CheckClickTransaction(ClickUz):
    """Zaka idsini va narxini tekshirish uchun"""

    def check_order(self, order_id: str, amount: str):
        try:
            transaction = ClickOrders.objects.get(id=int(order_id))
            if transaction.amount != Decimal(amount):
                return self.INVALID_AMOUNT
            transaction.verify()
        except ClickOrders.DoesNotExist:
            return self.ORDER_NOT_FOUND
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        try:
            transaction = ClickOrders.objects.get(id=int(order_id))
            transaction.make_payment()
        except ClickOrders.DoesNotExist:
            return
