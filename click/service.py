from .models import ClickOrder


def initialize_transaction(user, amount, transaction_type):
    obj = ClickOrder.objects.create(
        user=user,
        amount=amount,
        transaction_type=transaction_type,
    )
    print("ZAKAZ KIRITISH====", obj)
    return obj.id


def pay_transaction(transaction_id):
    try:
        instance = ClickOrder.objects.get(id=transaction_id)
        print("to'lov_tranzaksiyasi=====", instance)
        instance.make_payment()
    except ClickOrder.DoesNotExist:
        return


def cancel_transaction(transaction_id):
    try:
        instance = ClickOrder.objects.get(id=transaction_id)
        print("tranzaksiyani bekor qilish", instance)
        instance.cancel()
    except ClickOrder.DoesNotExist:
        return