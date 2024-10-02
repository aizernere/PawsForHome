from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_pet, name='add_pet'),
    path('list/', views.list_pet, name='list_pet'),
]