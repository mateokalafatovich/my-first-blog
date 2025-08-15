from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('search/', views.search_posts, name='search_posts'),
    path('tag/<slug:slug>/', views.posts_by_tag, name='posts_by_tag'),
]