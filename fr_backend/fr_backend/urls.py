# Django
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

# Django Rest Framework
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

# Project
from fr_backend import settings

router = routers.DefaultRouter()

urlpatterns = [
    url('', include(('apps.ui.urls', 'ui'), namespace='ui')),
    path(r'api/', include(('apps.api.urls', 'api'), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include_docs_urls(title="接口文档", authentication_classes=[], permission_classes=[])),
    path('admin/', admin.site.urls),
]

# 静态资源
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug tools
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls))
        ]
    except ImportError:
        pass
