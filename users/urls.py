# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('request-otp/', views.request_otp_view, name='request_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('profile/', views.user_profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]