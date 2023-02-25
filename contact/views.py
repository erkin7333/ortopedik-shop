from django.shortcuts import render, redirect
from .models import Contact, Requestforhelp
from .forms import RequestforhelpForm

# Create your views here.


def contact(request):
    contact = Contact.objects.get()
    if request.method == 'POST':
        form = RequestforhelpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact:contact")
    else:
        form = RequestforhelpForm()
    context = {
        'contact': contact,
        'form': form
    }
    return render(request, 'main/contact.html', context=context)