from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls', namespace='trucks-signs-root')),
    url(r'^truck-signs/', include('backend.urls', namespace='trucks-signs-api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
