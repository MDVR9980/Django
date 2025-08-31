from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from cart.cart_module import Cart

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "cart/cart_detail.html", {'cart': cart})
    

class CartAddView(View):
    def post(self, request, pk):
        # product = Product.objects.get(id=pk)
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = request.POST.get('size', "ندارد"), request.POST.get('color', 'ندارد'), request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect('cart:cart_detail')
    
class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')