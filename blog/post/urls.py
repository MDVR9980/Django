from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('detail/<int:pk>', views.post_detail, name='post_detail')
]
