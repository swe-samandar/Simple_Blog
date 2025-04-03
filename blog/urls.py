from django.urls import path
from .views import (
    PostsListView,
    AboutView,
    ContactViev,
    DetailView,
    SearchView,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
CommentCreateView
    ) 

app_name = 'blog'

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactViev.as_view(), name='contact'),
    path('detail/<int:pk>/', DetailView.as_view(), name='detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('post/new/', CreatePostView.as_view(), name='post_create'),
    path('post/<int:pk>/edit', UpdatePostView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='post_delete'),
    path('post/comment/', CommentCreateView.as_view(), name='comment')
]