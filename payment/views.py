from django.shortcuts import render
from main.models import Order


def payment_method(request):
    payment_p = Order.objects.filter(user=request.user).last()
    context = {
        'payment_p': payment_p
    }
    return render(request, 'main/payment.html', context=context)
