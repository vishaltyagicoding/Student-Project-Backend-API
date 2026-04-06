from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import APIDocumentationView, api_root

urlpatterns = [
    path('', APIDocumentationView.as_view(), name='api-documentation'),
    path('api/', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/students/', include('apps.students.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Student Manager Admin"
admin.site.site_title = "Student Manager Admin Portal"
admin.site.index_title = "Welcome to Student Manager Administration"