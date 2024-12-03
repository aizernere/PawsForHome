from django.urls import path
from . import views

urlpatterns = [
    path('send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('conversation/<int:receiver_id>/', views.view_conversation, name='view_conversation'),
    # path('accounts/', views.list_accounts, name='list_accounts'),
]