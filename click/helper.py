from .models import ClickOrder
from .service import pay_transaction, cancel_transaction
from clickuz import ClickUz
from decimal import Decimal


class CheckClickTransaction(ClickUz):
    def check_order(self, order_id: str, amount: str):
        try:
            transaction = ClickOrder.objects.get(id=int(order_id))
            print("SUMMANI TEKSHIRISH=====", transaction)
            if transaction.amount != Decimal(amount):
                return self.INVALID_AMOUNT
            transaction.verify()
        except ClickOrder.DoesNotExist:
            return
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        try:
            transaction = ClickOrder.objects.get(id=int(order_id))
            transaction.make_payment()
            print("SUCCESS=====", transaction)
        except ClickOrder.DoesNotExist:
            return