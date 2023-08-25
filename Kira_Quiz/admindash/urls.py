from django.contrib import admin
from django.urls import path
from .views import admin_dashboard, admin_login, adminback, admin_logout



urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('adminback/', adminback, name='adminback'),
    path('', admin_logout, name='admin_logout'),
    
]