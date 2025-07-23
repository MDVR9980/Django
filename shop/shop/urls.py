from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_app.urls')),
    path('account/', include('accounts_app.urls')),
    path('course/', include('courses_app.urls')),
    path('ticket/', include('tickets_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)