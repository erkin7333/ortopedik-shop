from django.shortcuts import render, redirect
from .models import Contact, Requestforhelp, Blog
from .forms import RequestforhelpForm

# Create your views here.


def contact(request):
    default_contact = "Hozircha malumot yoq"
    try:
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
    except Contact.DoesNotExist:
        context = {"contact": default_contact}
        return render(request, 'main/contact.html', context=context)


def blogpage(request):
    blog = Blog.objects.order_by('-id')
    context = {'blog': blog}
    return render(request, 'main/blog.html', context=context)

def blogdetail(request, pk):
    d_blog = Blog.objects.get(id=pk)
    context = {'d_blog': d_blog}
    return render(request, 'main/blog-detail.html', context=context)