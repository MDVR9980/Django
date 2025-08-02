from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('detail/<slug:slug>', views.post_detail, name='post_detail'),
    path('list', views.posts_list, name="posts_list"),
    path('category/<int:pk>', views.category_detail , name="category_detail"),
    path('search/', views.search, name="search_articles"),
    path('contactus/', views.contactus, name='contact_us'),
]
