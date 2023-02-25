from main.models import Category



def menucategory(request):
    categories = Category.objects.all()
    ctx = {
        'categories': categories
    }
    return ctx