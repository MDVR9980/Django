from django.urls import path
from . import views

urlpatterns = [
    path('list', views.course_list),
    path('detail/<int:id>', views.course_detail),
    path('add', views.add_course)
]
