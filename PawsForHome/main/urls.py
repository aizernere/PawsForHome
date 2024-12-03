from django.urls import path
from . import views
from pets.views import my_pets, dashpets, petsadopted, edit_pet, delete_pet, restore_pet
from pmessages.views import send_message, view_conversation, conversations_list

urlpatterns = [
    path('',views.landing_page,name='landing_page'), #none
    path('features/',views.features,name='features'), #none
    path('contactus/',views.contactus,name='contactus'), #none
    # path('index/', views.index, name='index'),
    path('notifications/', views.notifications, name='notifications'), #logged in
    path('message/', conversations_list, name='conversations_list'), #logged in
    path('profile/', views.profile, name='profile'), #logged in
    path('signup/', views.create_account, name='create_account'), #none
    path('login/',views.login_account, name='login_account'), #none
    path('logout/',views.logout_account, name='logout_account'),  #logged in
    path('home/',views.home, name='home'),  #logged in
    path('adoptionform/<int:pet_id>/',views.adoption_request_view, name='adoptionform'), #user's adoption request form
    # path('shelterdashboard/',views.shelterdashboard, name='shelterdashboard'),
    # path('pet_listings/', views.pet_listings, name='pet_listings'),
    path('adoptionrequest/<int:request_id>/', views.adoption_request_detail, name='adoption_request_detail'),  #shelter's adoption request view
    path('shelterdashboard/',dashpets, name='shelterdashboard'), #shelter
    path('petsadopted/',petsadopted, name='petsadopted'), #shelter
    path('pet_listings/', my_pets, name='pet_listings'), #shelter
    path('edit_pet/<int:pet_id>/', edit_pet, name='edit_pet'), #shelter
    path('delete_pet/<int:pet_id>/',delete_pet, name='delete_pet'), #shelter
    path('pending_requests/', views.pending_requests, name='pending_requests'), #shelter
    path('restore_pet/<int:pet_id>/', restore_pet, name='restore_pet'), #shelter
    #path('adoptform/', views.adoptform, name='adoptform'),
    path('profile_filling/', views.profile_filling, name='profile_filling'), #logged in
    path('userdashboard/',views.user_dashboard, name='user_dashboard'), #user
    path('requests/',views.ud_requests, name='ud_requests'),    #user
    path('favorites/',views.ud_favorites, name='ud_favorites'), #user
    path('adoptionhistory/',views.ud_adoptionhistory, name='ud_adoptionhistory'), #user
    path('error404/',views.error404, name='error404'), #none
]
