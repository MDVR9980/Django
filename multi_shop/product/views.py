from django.shortcuts import render
from django.views.generic import DeleteView, TemplateView, ListView
from product.models import Product, Category

class ProductDetailView(DeleteView):
    template_name = 'product/product_detail.html'
    model = Product
    
class NavbarPartialView(TemplateView):
    template_name = 'includes/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context
    
class CategoryStyle(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryStyle, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context
    
class CategoryStyle(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryStyle, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

from django.views.generic import ListView
from .models import Product

class ProductsListView(ListView):
    template_name = 'product/products_list.html'
    paginate_by = 3  # Number of products per page

    def get_queryset(self):
        # Get request parameters (filters)
        request = self.request
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Base queryset
        queryset = Product.objects.all()

        # Filter by colors (if any are selected)
        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()

        # Filter by sizes (if any are selected)
        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()

        # Filter by price range (if both min and max are provided)
        if min_price and max_price:
            queryset = queryset.filter(price__lte=max_price, price__gte=min_price).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add current querystring to context (to keep filters while paginating)
        context['querystring'] = self.request.GET.urlencode()
        # Also pass filters to template so checkboxes remain checked
        context['selected_colors'] = self.request.GET.getlist('color')
        context['selected_sizes'] = self.request.GET.getlist('size')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        return context
