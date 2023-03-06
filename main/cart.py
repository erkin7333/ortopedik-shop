from django.conf import settings
from .models import Products



class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Products.objects.get(pk=p)

        for item in self.cart.values():
            product = item['product']
            item['total_price'] = int(product.price * item['quantity'])
            item['number'] = str(product.number)
            item['price'] = str(product.price)
            item['color'] = str(item['color'])
            item['size'] = str(item['size'])
            # item['size'] = ', '.join(size for size in product.size.values_list(str('size'), flat=True))
            # item['name'] = str(product.name)
            # item['created_at'] = str(product.created_at)
            # item['price'] = int(product.price)
            # item['color'] = ', '.join(color for color in product.color.values_list(str('name'), flat=True))

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def add(self, product_id, quantity=1, update_quantity=False, color=None, size=None, number=None, price=None):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': int(quantity), 'id': product_id,
                                     'color': color, 'size': size,
                                     "price": price, 'number': number}
            self.save()
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
                self.save()

        self.save()


    def remove(self, product_id):
        if str(product_id) in self.cart:
            del self.cart[product_id]

            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Products.objects.get(pk=p)

        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values()))
