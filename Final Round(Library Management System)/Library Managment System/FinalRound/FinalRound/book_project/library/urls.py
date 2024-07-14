from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_books, name='search_books'),
    path('add_to_store/', views.add_to_store, name='add_to_store'),
]



