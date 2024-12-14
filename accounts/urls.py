from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user_created_posts', views.user_created_posts, name='user_created_posts'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
]