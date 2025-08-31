from django.shortcuts import render
from django.views.generic import DeleteView
from product.models import Product
class ProductDetailView(DeleteView):
    template_name = 'product/product_detail.html'
    model = Product
    