
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Inventory import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('master.urls')),
    path('', include('operations.urls')),
    path('', include('reports.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


