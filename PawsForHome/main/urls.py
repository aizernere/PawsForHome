from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing_page,name='landing_page'),
    path('index/', views.index, name='index'),
    path('notifications/', views.notifications, name='notifications'),
    path('message/', views.message, name='message'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.create_account, name='create_account'),
    path('login/',views.login_account, name='login_account'),
    path('logout/',views.logout_account, name='logout_account'),  
    path('home/',views.home, name='home'),    
    path('adoptionform/',views.adoptionform, name='adoptionform'),
]