from django.urls import path
from . import views
from pets.views import my_pets, dashpets

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
    path('adoptionform/<int:pet_id>/',views.adoption_request_view, name='adoptionform'),
    # path('shelterdashboard/',views.shelterdashboard, name='shelterdashboard'),
    # path('pet_listings/', views.pet_listings, name='pet_listings'),
    path('shelterdashboard/',dashpets, name='shelterdashboard'),
    path('pet_listings/', my_pets, name='pet_listings'),
    path('pending_requests/', views.pending_requests, name='pending_requests'),
    path('adoptform/', views.adoptform, name='adoptform'),
    path('profile_filling/', views.profile_filling, name='profile_filling'),
    path('userdashboard/',views.user_dashboard, name='user_dashboard'),
    path('requests/',views.ud_requests, name='ud_requests'),
    path('favorites/',views.ud_favorites, name='ud_favorites'),
    path('adoptionhistory/',views.ud_adoptionhistory, name='ud_adoptionhistory'),
]
