from django.urls import path
from . import views

app_name = 'usr'

urlpatterns = [
    path('otp_verification/', views.send_otp_email_verification),
    path('register/', views.register),
    path('login/', views.login),
]
