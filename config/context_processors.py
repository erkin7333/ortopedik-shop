from main.models import Category
from contact.models import Contact
from main.cart import Cart


def menucategory(request):
    categories = Category.objects.all()
    ctx = {
        'categories': categories
    }
    return ctx


def getphone(request):
    default_phone = "+99890 123-45-67"
    try:
        contact = Contact.objects.first()
        sphone = contact.phone
        sphone1 = contact.phone1
    except AttributeError:
        sphone = default_phone
        sphone1 = default_phone
    ctx = {'sphone': sphone, 'sphone1': sphone1}
    return ctx


def getcartcount(request):
    default_count = "0"
    try:
        cart_count = Cart(request)
        scount = len(cart_count)
        cxt = {'scount': scount}
        return cxt
    except Cart.DoesNotExist:
        cxt = {'cart_count': default_count}
        return cxt
