from .models import ClickOrders




def initialize_transaction(user, amount, transaction_type):
    obj = ClickOrders.objects.create(user=user, amount=amount, transaction_type=transaction_type)
    return obj.id


def pay_transaction(transaction_id):
    try:
        instance = ClickOrders.objects.get(id=transaction_id)
        instance.make_payment()
    except ClickOrders.DoesNotExist:
        return


def cancel_transaction(transaction_id):
    try:
        instance = ClickOrders.objects.get(id=transaction_id)
        instance.cancel()
    except ClickOrders.DoesNotExist:
        return
