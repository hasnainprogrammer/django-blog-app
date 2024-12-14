from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='posts'),
    path('<int:post_id>', views.post, name='post'),
    path('makepost', views.makepost, name='makepost'),
    path('search', views.search, name='search'),
]