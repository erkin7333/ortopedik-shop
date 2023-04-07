from .models import ClickOrder


def initialize_transaction(user, amount, transaction_type):
    obj = ClickOrder.objects.create(user=user, amount=amount, transaction_type=transaction_type)
    return obj.id


def pay_transaction(transaction_id):
    try:
        instance = ClickOrder.objects.get(id=transaction_id)
        instance.make_payment()
    except ClickOrder.DoesNotExist:
        return


def cancel_transaction(transaction_id):
    try:
        instance = ClickOrder.objects.get(id=transaction_id)
        instance.cancel()
    except ClickOrder.DoesNotExist:
        return
