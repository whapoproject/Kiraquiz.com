from django.urls import path
from . import views

app_name = 'userdash'

urlpatterns = [
    path('', views.userdash_home, name='userdash_home'),  
    path('profile/', views.user_profile, name='user_profile'),
    path('real-account/', views.real_account, name='real_account'),
    path('demo-account/', views.demo_account, name='demo_account'),
    path('quizzes/', views.quizzes, name='quizzes'),
]
