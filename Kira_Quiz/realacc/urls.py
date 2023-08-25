from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetCompleteView,
)



urlpatterns = [
  
    path('', views.user_register, name='user_register'),

    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    
    path('login/',  views.user_login, name='user_login'),
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
 

    path('real_account/',  views.real_account, name='real_account'),

    path('transactions/paid_quizzes/', views.paid_quizzes, name='paid_quizzes'),
    path('transactions/pay_quizzes/', views.pay_quizzes, name='pay_quizzes'),

    path('transactions/deposits/', views.deposits, name='deposits'),
    path('transactions/withdraws/', views.withdraws, name='withdraws'),

    path('payment/',  views.payment, name='payment'),
    path('payment1/',  views.payment1, name='payment1'),
    path('payment2/',  views.payment2, name='payment2'),  
]


