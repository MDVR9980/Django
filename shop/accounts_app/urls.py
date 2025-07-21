from django.urls import path
from . import views 

urlpatterns = [
    path('info', views.info),
    path('profile/<username>', views.profile),
    path('userslist', views.userslist),
]