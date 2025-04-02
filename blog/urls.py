from django.urls import path
from .views import (
    PostsListView,
    AboutView,
    ContactViev,
    DetailView,
    SearchView,
    ) 

app_name = 'blog'

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactViev.as_view(), name='contact'),
    path('detail/<int:pk>/', DetailView.as_view(), name='detail'),
    path('search/', SearchView.as_view(), name='search'),
]