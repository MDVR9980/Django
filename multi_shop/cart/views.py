from django.shortcuts import render, redirect
from django.views import View

class CartDetailView(View):
    def get(self, request):
        return render(request, "cart/cart_detail.html", {})
    

class CartAddView(View):
    def post(self, request):
        print("product added")
        return redirect('cart:cart_detail')