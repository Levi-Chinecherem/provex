# main_p/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('static_pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('estate.urls')),
    path('payment/', include('payment.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
