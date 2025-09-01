from product.models import Product

CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            item['unique_id'] = self.unique_id_generator(product.id, item['color'], item['size'])
            yield item

    def unique_id_generator(self, id, color, size):
        result = f'{id}-{color}-{size}'
        return result

    def remove_cart(self):
        del self.session[CART_SESSION_ID]
        
    def add(self, product, quantity, color, size):
        unique = self.unique_id_generator(product.id, color, size)
        if unique not in self.cart:
            self.cart[unique] = {'quantity': 0, 'price': str(product.price), 'color': color, 'size': size, 'id': product.id}
        
        self.cart[unique]['quantity'] += int(quantity)
        self.save()
    
    def total(self):
        cart = self.cart.values()
        # total = sum(int(item['price'] )* int(item['quantity']) for item in cart)
        total = 0
        for item in cart:
            total += int(item['price'] )* int(item['quantity'])
        return total

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True