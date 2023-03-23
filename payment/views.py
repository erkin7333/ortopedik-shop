from django.shortcuts import render
from payment.models import PaymentOrder


def payment_method(request):
    payment_p = PaymentOrder.objects.filter(user=request.user).last()
    context = {
        'payment_p': payment_p
    }
    return render(request, 'main/payment.html', context=context)
