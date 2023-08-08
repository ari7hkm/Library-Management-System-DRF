from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'Library Admin'
admin.site.index_title = 'Admin'
admin.site.site_title = 'Library'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)