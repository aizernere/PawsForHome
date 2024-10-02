from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('browse/', views.browse, name='browse'),
    path('notifications/', views.notifications, name='notifications'),
    path('message/', views.message, name='message'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.create_account, name='create_account'),
]