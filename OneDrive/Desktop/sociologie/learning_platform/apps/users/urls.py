from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet
from .auth_views import (
    login_view, signup_view, logout_view, token_refresh_view,
    password_reset_request_view, password_reset_confirm_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', token_refresh_view, name='token_refresh'),
    path('password-reset/', password_reset_request_view, name='password_reset'),
    path('password-reset-confirm/', password_reset_confirm_view, name='password_reset_confirm'),
]

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')
router.register(r'profiles', UserProfileViewSet, basename='profiles')

urlpatterns += router.urls
