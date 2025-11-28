from django.urls import path, include, re_path
from django.contrib import admin
from .views import FrontendAppView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/exercises/', include('apps.exercises.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/recommendations/', include('apps.recommendations.urls')),
    path('api/emotions/', include('apps.emotions.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    # Toutes les autres routes vers la build React (pour le routing côté client)
    re_path(r'^(?!api/|admin/|static/|media/).*$', FrontendAppView.as_view(), name='frontend_app'),
]
