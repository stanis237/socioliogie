"""
URL Configuration pour Swagger/OpenAPI
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Plateforme d'Apprentissage IA API",
        default_version='v1',
        description="API REST pour la plateforme d'apprentissage personnalisé avec IA",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@learning-platform.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/exercises/', include('apps.exercises.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/recommendations/', include('apps.recommendations.urls')),
    path('api/emotions/', include('apps.emotions.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
