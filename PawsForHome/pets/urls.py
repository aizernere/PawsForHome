from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_pet, name='add_pet'),
    path('list/', views.list_pet, name='list_pet'),
    path('adoption/accept/<int:request_id>/', views.accept_adoption_request, name='accept_adoption_request'),
    path('adoption/reject/<int:request_id>/', views.reject_adoption_request, name='reject_adoption_request'),
    path('toggle_favorite/<int:pet_id>/', views.toggle_favorite, name='toggle_favorite'),
]