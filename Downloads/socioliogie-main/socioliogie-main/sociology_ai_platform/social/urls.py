from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.forum, name='forum'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('notifications/', views.notifications, name='notifications'),
]

