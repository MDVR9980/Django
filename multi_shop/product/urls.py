from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('<int:pk>', views.ProductDetailView.as_view() , name="product_detail"),
]
