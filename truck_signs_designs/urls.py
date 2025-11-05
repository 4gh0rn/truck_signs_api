from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from backend.views import homepage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('api/', include('backend.urls', namespace='trucks-signs-root')),
    url(r'^truck-signs/', include('backend.urls', namespace='trucks-signs-api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
